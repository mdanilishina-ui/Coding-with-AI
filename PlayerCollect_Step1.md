# Player Collect Mechanic — Step 1: Create `AThirdPersonCharacter` (with `APlayerCharacter` alias)

## Files Created
- `Source/MyProject/Player/ThirdPersonCharacter.h`
- `Source/MyProject/Player/ThirdPersonCharacter.cpp`
- `Source/MyProject/Player/PlayerCharacter.h`
- `Source/MyProject/Player/PlayerCharacter.cpp`

> Replace `MyProject` with your module name if it differs. Keep the folder path consistent inside the module (e.g., `Source/MyProject/Player/`).

## Architecture Rationale
- **Owner**: The player-controlled pawn should be an `ACharacter` to leverage the Character Movement Component for built-in walking, jumping, and navigation support.
- **Responsibility**: This class owns input bindings (jump, movement, and a temporary TestLog action) and basic logging to prove the pawn and input are wired correctly in C++ only (no Blueprint dependency).
- **Compatibility**: `APlayerCharacter` subclasses `AThirdPersonCharacter` to keep the original class name available for branches that still reference it, reducing merge conflicts while preserving the new template-aligned setup.
- **Dependency**: Uses `UCharacterMovementComponent` already on `ACharacter`; no extra components required for this step.

## C++ Code

### `ThirdPersonCharacter.h`
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ThirdPersonCharacter.generated.h"

UCLASS()
class MYPROJECT_API AThirdPersonCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AThirdPersonCharacter();

protected:
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

private:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void HandleTestLog();
};
```

### `ThirdPersonCharacter.cpp`
```cpp
#include "ThirdPersonCharacter.h"
#include "GameFramework/Controller.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/InputComponent.h"

AThirdPersonCharacter::AThirdPersonCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    // Align capsule and controller rotation with the basic ThirdPerson template.
    GetCapsuleComponent()->InitCapsuleSize(42.f, 96.f);

    bUseControllerRotationPitch = false;
    bUseControllerRotationYaw = false;
    bUseControllerRotationRoll = false;

    // Third-person camera boom + follow camera matching UE's starter asset names.
    USpringArmComponent* SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->TargetArmLength = 300.f;
    SpringArm->bUsePawnControlRotation = true;

    UCameraComponent* FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;

    // Basic ThirdPerson Character Movement defaults.
    UCharacterMovementComponent* MoveComp = GetCharacterMovement();
    if (MoveComp)
    {
        MoveComp->bOrientRotationToMovement = true;
        MoveComp->RotationRate = FRotator(0.f, 540.f, 0.f);
        MoveComp->JumpZVelocity = 700.f;
        MoveComp->AirControl = 0.35f;
        MoveComp->MaxWalkSpeed = 600.f;
        MoveComp->BrakingDecelerationWalking = 2048.f;
    }
}

void AThirdPersonCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    check(PlayerInputComponent);

    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Pressed, this, &ACharacter::Jump);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Released, this, &ACharacter::StopJumping);

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &AThirdPersonCharacter::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &AThirdPersonCharacter::MoveRight);

    PlayerInputComponent->BindAction(TEXT("TestLog"), IE_Pressed, this, &AThirdPersonCharacter::HandleTestLog);
}

void AThirdPersonCharacter::MoveForward(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRot = Controller->GetControlRotation();
        const FRotator YawRot(0.f, ControlRot.Yaw, 0.f);

        const FVector Direction = FRotationMatrix(YawRot).GetUnitAxis(EAxis::X);
        AddMovementInput(Direction, Value);
    }
}

void AThirdPersonCharacter::MoveRight(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRot = Controller->GetControlRotation();
        const FRotator YawRot(0.f, ControlRot.Yaw, 0.f);

        const FVector Direction = FRotationMatrix(YawRot).GetUnitAxis(EAxis::Y);
        AddMovementInput(Direction, Value);
    }
}

void AThirdPersonCharacter::HandleTestLog()
{
    UE_LOG(LogTemp, Log, TEXT("TestLog input received on %s"), *GetName());
}
```

### `PlayerCharacter.h/.cpp` (compatibility wrapper)
```cpp
#pragma once

#include "CoreMinimal.h"
#include "ThirdPersonCharacter.h"
#include "PlayerCharacter.generated.h"

UCLASS()
class MYPROJECT_API APlayerCharacter : public AThirdPersonCharacter
{
    GENERATED_BODY()

public:
    APlayerCharacter();
};
```

```cpp
#include "PlayerCharacter.h"

APlayerCharacter::APlayerCharacter()
    : Super()
{
    // Intentionally relies on AThirdPersonCharacter defaults to match the ThirdPerson template
    // while keeping the legacy class name available.
}
```

## Editor Setup (UE5)
1. Add the new class files to your module, then compile.
2. In Project Settings → Input:
   - **Action**: `Jump` mapped to Spacebar (default) and `TestLog` mapped to a convenient key (e.g., `T`).
   - **Axis**: `MoveForward` (W/S or Up/Down, Scale 1/-1), `MoveRight` (A/D or Left/Right, Scale -1/1).
3. If you are working from the basic ThirdPerson template assets, create or reuse `BP_ThirdPersonCharacter` (or your existing starter blueprint) derived from `AThirdPersonCharacter` so its mesh/anim blueprint stay intact. Projects that still reference `BP_PlayerCharacter` can keep that blueprint by switching its parent to `APlayerCharacter` to avoid merge conflicts.
4. Set `AThirdPersonCharacter` (or your `BP_ThirdPersonCharacter`) as the default pawn class in your GameMode and place the pawn in the level if needed. Teams that still need the legacy name can set `APlayerCharacter`/`BP_PlayerCharacter` instead; both share the same behavior.

## Tests
- Play In Editor, move with configured keys; character should walk using Character Movement.
- Press the TestLog key; Output Log should print `TestLog input received on <PawnName>` confirming input binding.

## Fallbacks / Tips
- If movement axes do nothing, re-check Project Settings → Input axis names and key scales.
- If the log never appears, ensure the pawn is possessed (auto-possess or via GameMode) and that `TestLog` action name matches the binding exactly.
- If camera is missing, ensure SpringArm/Camera subobjects remain in the class or attach your own camera in a derived Blueprint.
