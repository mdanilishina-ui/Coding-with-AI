"""
UE5 Python setup script for the Coding_with_Ai project.
Run this inside the Unreal Editor's Python console to scaffold the C++ gameplay classes
needed for the third-person collection, AI pursuit, and shader feedback mechanics.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

PROJECT_NAME = "Coding_with_Ai"
MODULE_API = "CODING_WITH_AI_API"


class CodingWithAiSetup:
    """Writes the C++ scaffolding for the Coding_with_Ai prototype.

    The script creates the UE5 C++ source tree with the following gameplay classes:
    * AAgentKaiCharacter      – playable hero with grab-and-attach collection logic.
    * ACollectibleItem        – pickup actor that can be attached to the hero's back.
    * AEnemyAICharacter       – pursuer pawn configured for AI control.
    * AEnemyAIController      – sight-based perception and chase/search behavior.
    * AProgressShaderManager  – dynamic material updater for distance + progress heat.
    """

    def __init__(self, project_root: Path | str | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parents[1]).resolve()
        self.source_root = self.project_root / "Source" / PROJECT_NAME
        self.public_dir = self.source_root / "Public"
        self.private_dir = self.source_root / "Private"

    # ----------------------------------------------------------------------------------
    # Entry point
    # ----------------------------------------------------------------------------------
    def run(self) -> None:
        self._ensure_directories()
        self._write_build_cs()
        self._write_player_character()
        self._write_collectible_item()
        self._write_enemy_ai_character()
        self._write_enemy_ai_controller()
        self._write_shader_manager()
        print("Coding_with_Ai C++ scaffolding generated. Review and build from the UE5 Editor.")

    # ----------------------------------------------------------------------------------
    # Filesystem helpers
    # ----------------------------------------------------------------------------------
    def _ensure_directories(self) -> None:
        for path in [self.source_root, self.public_dir, self.private_dir]:
            path.mkdir(parents=True, exist_ok=True)
        print(f"Ensured source directories under {self.source_root}")

    def _write_file(self, relative_path: Path, content: str) -> None:
        full_path = self.source_root / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with full_path.open("w", encoding="utf-8") as file:
            file.write(dedent(content).strip() + "\n")
        print(f"Wrote {full_path.relative_to(self.project_root)}")

    # ----------------------------------------------------------------------------------
    # Build.cs
    # ----------------------------------------------------------------------------------
    def _write_build_cs(self) -> None:
        content = f'''
            using UnrealBuildTool;
            
            public class {PROJECT_NAME} : ModuleRules
            {{
                public {PROJECT_NAME}(ReadOnlyTargetRules Target) : base(Target)
                {{
                    PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

                    PublicDependencyModuleNames.AddRange(new string[]
                    {{
                        "Core",
                        "CoreUObject",
                        "Engine",
                        "InputCore",
                        "AIModule",
                        "GameplayTasks",
                        "UMG"
                    }});

                    PrivateDependencyModuleNames.AddRange(new string[] {{ }});
                }}
            }}
        '''
        self._write_file(Path(f"../{PROJECT_NAME}.Build.cs"), content)

    # ----------------------------------------------------------------------------------
    # Player character
    # ----------------------------------------------------------------------------------
    def _write_player_character(self) -> None:
        header = f'''
            #pragma once

            #include "CoreMinimal.h"
            #include "GameFramework/Character.h"
            #include "AgentKaiCharacter.generated.h"

            class USpringArmComponent;
            class UCameraComponent;
            class ACollectibleItem;

            UCLASS()
            class {MODULE_API} AAgentKaiCharacter : public ACharacter
            {{
                GENERATED_BODY()

            public:
                AAgentKaiCharacter();

                virtual void Tick(float DeltaTime) override;
                virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

            protected:
                virtual void BeginPlay() override;

                void MoveForward(float Value);
                void MoveRight(float Value);
                void TestLogAction();
                void StartGrab();
                void TryCollectItem();

                UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
                USpringArmComponent* CameraBoom;

                UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
                UCameraComponent* FollowCamera;

                UPROPERTY(EditDefaultsOnly, Category = "Collecting")
                float GrabDistance;

                UPROPERTY(EditDefaultsOnly, Category = "Collecting")
                float GrabRadius;

            }};
        '''

        source = f'''
            #include "Characters/AgentKaiCharacter.h"

            #include "Camera/CameraComponent.h"
            #include "Collectibles/CollectibleItem.h"
            #include "GameFramework/SpringArmComponent.h"
            #include "Kismet/KismetSystemLibrary.h"
            #include "DrawDebugHelpers.h"

            AAgentKaiCharacter::AAgentKaiCharacter()
            {{
                PrimaryActorTick.bCanEverTick = true;

                CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
                CameraBoom->SetupAttachment(RootComponent);
                CameraBoom->TargetArmLength = 300.0f;
                CameraBoom->bUsePawnControlRotation = true;

                FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
                FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
                FollowCamera->bUsePawnControlRotation = false;

                GrabDistance = 250.0f;
                GrabRadius = 60.0f;
            }}

            void AAgentKaiCharacter::BeginPlay()
            {{
                Super::BeginPlay();
                UE_LOG(LogTemp, Log, TEXT("AgentKai ready for collection tests."));
            }}

            void AAgentKaiCharacter::Tick(float DeltaTime)
            {{
                Super::Tick(DeltaTime);
            }}

            void AAgentKaiCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
            {{
                Super::SetupPlayerInputComponent(PlayerInputComponent);
                check(PlayerInputComponent);

                PlayerInputComponent->BindAxis("MoveForward", this, &AAgentKaiCharacter::MoveForward);
                PlayerInputComponent->BindAxis("MoveRight", this, &AAgentKaiCharacter::MoveRight);
                PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
                PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);
                PlayerInputComponent->BindAction("TestLog", IE_Pressed, this, &AAgentKaiCharacter::TestLogAction);
                PlayerInputComponent->BindAction("Grab", IE_Pressed, this, &AAgentKaiCharacter::StartGrab);
            }}

            void AAgentKaiCharacter::MoveForward(float Value)
            {{
                if (Controller && FMath::Abs(Value) > KINDA_SMALL_NUMBER)
                {{
                    const FRotator ControlRotation = Controller->GetControlRotation();
                    const FRotator YawRotation(0.f, ControlRotation.Yaw, 0.f);

                    const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
                    AddMovementInput(Direction, Value);
                }}
            }}

            void AAgentKaiCharacter::MoveRight(float Value)
            {{
                if (Controller && FMath::Abs(Value) > KINDA_SMALL_NUMBER)
                {{
                    const FRotator ControlRotation = Controller->GetControlRotation();
                    const FRotator YawRotation(0.f, ControlRotation.Yaw, 0.f);

                    const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
                    AddMovementInput(Direction, Value);
                }}
            }}

            void AAgentKaiCharacter::TestLogAction()
            {{
                UE_LOG(LogTemp, Log, TEXT("TestLog action pressed — input mapping confirmed."));
            }}

            void AAgentKaiCharacter::StartGrab()
            {{
                TryCollectItem();
            }}

            void AAgentKaiCharacter::TryCollectItem()
            {{
                const FVector Start = FollowCamera->GetComponentLocation();
                const FVector End = Start + FollowCamera->GetForwardVector() * GrabDistance;

                FHitResult HitResult;
                const bool bHit = UKismetSystemLibrary::SphereTraceSingle(
                    GetWorld(),
                    Start,
                    End,
                    GrabRadius,
                    UEngineTypes::ConvertToTraceType(ECC_Visibility),
                    false,
                    {{ this }},
                    EDrawDebugTrace::ForDuration,
                    HitResult,
                    true);

                if (bHit)
                {{
                    UE_LOG(LogTemp, Log, TEXT("Grab trace hit: %s"), *GetNameSafe(HitResult.GetActor()));
                }}
                else
                {{
                    UE_LOG(LogTemp, Verbose, TEXT("Grab trace found nothing."));
                }}
            }}

        '''

        self._write_file(Path("Public/Characters/AgentKaiCharacter.h"), header)
        self._write_file(Path("Private/Characters/AgentKaiCharacter.cpp"), source)

    # ----------------------------------------------------------------------------------
    # Collectible item
    # ----------------------------------------------------------------------------------
    def _write_collectible_item(self) -> None:
        header = f'''
            #pragma once

            #include "CoreMinimal.h"
            #include "GameFramework/Actor.h"
            #include "CollectibleItem.generated.h"

            UCLASS()
            class {MODULE_API} ACollectibleItem : public AActor
            {{
                GENERATED_BODY()
            
            public:
                ACollectibleItem();

                void OnCollected();

            protected:
                UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Item")
                UStaticMeshComponent* ItemMesh;
            }};
        '''

        source = f'''
            #include "Collectibles/CollectibleItem.h"

            #include "Components/StaticMeshComponent.h"

            ACollectibleItem::ACollectibleItem()
            {{
                PrimaryActorTick.bCanEverTick = false;

                ItemMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ItemMesh"));
                ItemMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
                ItemMesh->SetSimulatePhysics(true);
                SetRootComponent(ItemMesh);
            }}

            void ACollectibleItem::OnCollected()
            {{
                ItemMesh->SetSimulatePhysics(false);
                SetActorEnableCollision(false);
            }}
        '''

        self._write_file(Path("Public/Collectibles/CollectibleItem.h"), header)
        self._write_file(Path("Private/Collectibles/CollectibleItem.cpp"), source)

    # ----------------------------------------------------------------------------------
    # Enemy AI character
    # ----------------------------------------------------------------------------------
    def _write_enemy_ai_character(self) -> None:
        header = f'''
            #pragma once

            #include "CoreMinimal.h"
            #include "GameFramework/Character.h"
            #include "EnemyAICharacter.generated.h"

            UCLASS()
            class {MODULE_API} AEnemyAICharacter : public ACharacter
            {{
                GENERATED_BODY()

            public:
                AEnemyAICharacter();
            }};
        '''

        source = f'''
            #include "Characters/EnemyAICharacter.h"

            AEnemyAICharacter::AEnemyAICharacter()
            {{
                PrimaryActorTick.bCanEverTick = false;
                AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
            }}
        '''

        self._write_file(Path("Public/Characters/EnemyAICharacter.h"), header)
        self._write_file(Path("Private/Characters/EnemyAICharacter.cpp"), source)

    # ----------------------------------------------------------------------------------
    # Enemy AI controller
    # ----------------------------------------------------------------------------------
    def _write_enemy_ai_controller(self) -> None:
        header = f'''
            #pragma once

            #include "CoreMinimal.h"
            #include "AIController.h"
            #include "EnemyAIController.generated.h"

            class UAIPerceptionComponent;
            class UAISenseConfig_Sight;

            UCLASS()
            class {MODULE_API} AEnemyAIController : public AAIController
            {{
                GENERATED_BODY()

            public:
                AEnemyAIController();

            protected:
                virtual void OnPossess(APawn* InPawn) override;

                UFUNCTION()
                void HandleTargetPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus);

                void BeginSearch();
                void SearchTick();

                UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AI")
                UAIPerceptionComponent* PerceptionComponent;

                UPROPERTY()
                UAISenseConfig_Sight* SightConfig;

                UPROPERTY()
                FTimerHandle SearchTimerHandle;

                UPROPERTY(EditDefaultsOnly, Category = "AI")
                float SearchDuration;
            }};
        '''

        source = f'''
            #include "AI/EnemyAIController.h"

            #include "Perception/AIPerceptionComponent.h"
            #include "Perception/AISenseConfig_Sight.h"
            #include "Perception/AISense_Sight.h"
            #include "Kismet/GameplayStatics.h"

            AEnemyAIController::AEnemyAIController()
            {{
                PerceptionComponent = CreateDefaultSubobject<UAIPerceptionComponent>(TEXT("PerceptionComponent"));
                SetPerceptionComponent(*PerceptionComponent);

                SightConfig = CreateDefaultSubobject<UAISenseConfig_Sight>(TEXT("SightConfig"));
                SightConfig->SightRadius = 900.0f;
                SightConfig->LoseSightRadius = 1200.0f;
                SightConfig->PeripheralVisionAngleDegrees = 75.0f;
                SightConfig->SetMaxAge(5.0f);
                SightConfig->DetectionByAffiliation.bDetectEnemies = true;
                SightConfig->DetectionByAffiliation.bDetectFriendlies = true;
                SightConfig->DetectionByAffiliation.bDetectNeutrals = true;

                PerceptionComponent->ConfigureSense(*SightConfig);
                PerceptionComponent->SetDominantSense(SightConfig->GetSenseImplementation());
                PerceptionComponent->OnTargetPerceptionUpdated.AddDynamic(this, &AEnemyAIController::HandleTargetPerceptionUpdated);

                SearchDuration = 60.0f;
            }}

            void AEnemyAIController::OnPossess(APawn* InPawn)
            {{
                Super::OnPossess(InPawn);
                UE_LOG(LogTemp, Log, TEXT("EnemyAIController possessed %s"), *GetNameSafe(InPawn));
            }}

            void AEnemyAIController::HandleTargetPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus)
            {{
                if (!Actor)
                {{
                    return;
                }}

                if (Stimulus.WasSuccessfullySensed())
                {{
                    UE_LOG(LogTemp, Log, TEXT("Player seen: %s"), *Actor->GetName());
                    MoveToActor(Actor, 75.0f);
                    GetWorld()->GetTimerManager().ClearTimer(SearchTimerHandle);
                }}
                else
                {{
                    UE_LOG(LogTemp, Log, TEXT("Player lost: %s"), *Actor->GetName());
                    BeginSearch();
                }}
            }}

            void AEnemyAIController::BeginSearch()
            {{
                GetWorld()->GetTimerManager().SetTimer(SearchTimerHandle, this, &AEnemyAIController::SearchTick, 2.5f, true);
                GetWorld()->GetTimerManager().SetTimerForNextTick([this]()
                {{
                    SearchTick();
                }});
            }}

            void AEnemyAIController::SearchTick()
            {{
                if (!GetPawn())
                {{
                    return;
                }}

                const FVector Origin = GetPawn()->GetActorLocation();
                const FVector RandomPoint = Origin + FMath::VRand() * 600.0f;
                MoveToLocation(RandomPoint);

                const float Elapsed = GetWorld()->GetTimerManager().GetTimerElapsed(SearchTimerHandle);
                if (Elapsed > SearchDuration)
                {{
                    GetWorld()->GetTimerManager().ClearTimer(SearchTimerHandle);
                }}
            }}
        '''

        self._write_file(Path("Public/AI/EnemyAIController.h"), header)
        self._write_file(Path("Private/AI/EnemyAIController.cpp"), source)

    # ----------------------------------------------------------------------------------
    # Shader distance feedback
    # ----------------------------------------------------------------------------------
    def _write_shader_manager(self) -> None:
        header = f'''
            #pragma once

            #include "CoreMinimal.h"
            #include "GameFramework/Actor.h"
            #include "ProgressShaderManager.generated.h"

            class UMaterialInstanceDynamic;
            class UStaticMeshComponent;

            UCLASS()
            class {MODULE_API} AProgressShaderManager : public AActor
            {{
                GENERATED_BODY()

            public:
                AProgressShaderManager();

                virtual void Tick(float DeltaTime) override;

            protected:
                virtual void BeginPlay() override;

                UFUNCTION(BlueprintCallable, Category = "Shader")
                void RefreshHeat();

                UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Shader")
                UStaticMeshComponent* PreviewMesh;

                UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shader")
                AActor* PlayerActor;

                UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shader")
                AActor* TargetActor;

                UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shader")
                float WarmDistance;

                UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shader")
                float CoolDistance;

                UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shader")
                float CollectedIntensityScale;

                UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shader")
                UMaterialInterface* BaseMaterial;

                UPROPERTY()
                UMaterialInstanceDynamic* DynamicMaterial;

                int32 CachedCollectedCount;
            }};
        '''

        source = f'''
            #include "Shaders/ProgressShaderManager.h"

            #include "Characters/AgentKaiCharacter.h"
            #include "Collectibles/CollectibleItem.h"
            #include "Components/StaticMeshComponent.h"
            #include "Materials/MaterialInstanceDynamic.h"
            #include "Kismet/KismetMathLibrary.h"

            AProgressShaderManager::AProgressShaderManager()
            {{
                PrimaryActorTick.bCanEverTick = true;

                PreviewMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PreviewMesh"));
                SetRootComponent(PreviewMesh);

                WarmDistance = 200.0f;
                CoolDistance = 1200.0f;
                CollectedIntensityScale = 0.15f;
                CachedCollectedCount = 0;
            }}

            void AProgressShaderManager::BeginPlay()
            {{
                Super::BeginPlay();

                if (BaseMaterial)
                {{
                    DynamicMaterial = UMaterialInstanceDynamic::Create(BaseMaterial, this);
                    PreviewMesh->SetMaterial(0, DynamicMaterial);
                }}

                RefreshHeat();
            }}

            void AProgressShaderManager::Tick(float DeltaTime)
            {{
                Super::Tick(DeltaTime);
                RefreshHeat();
            }}

            void AProgressShaderManager::RefreshHeat()
            {{
                if (!DynamicMaterial || !PlayerActor || !TargetActor)
                {{
                    return;
                }}

                const float Distance = FVector::Distance(PlayerActor->GetActorLocation(), TargetActor->GetActorLocation());
                const float HeatAlpha = UKismetMathLibrary::MapRangeClamped(Distance, WarmDistance, CoolDistance, 1.0f, 0.0f);

                float Intensity = HeatAlpha;
                if (const AAgentKaiCharacter* Agent = Cast<AAgentKaiCharacter>(PlayerActor))
                {{
                    const int32 NewCount = Agent->GetMesh() ? Agent->GetMesh()->GetNumChildrenComponents() : CachedCollectedCount;
                    CachedCollectedCount = NewCount;
                    Intensity += NewCount * CollectedIntensityScale;
                }}

                DynamicMaterial->SetScalarParameterValue(TEXT("HeatValue"), HeatAlpha);
                DynamicMaterial->SetScalarParameterValue(TEXT("HeatIntensity"), Intensity);
            }}
        '''

        self._write_file(Path("Public/Shaders/ProgressShaderManager.h"), header)
        self._write_file(Path("Private/Shaders/ProgressShaderManager.cpp"), source)


if __name__ == "__main__":
    setup = CodingWithAiSetup()
    setup.run()
