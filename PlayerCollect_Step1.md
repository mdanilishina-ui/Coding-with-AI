# Player Collect Mechanic — Step 1: Use the Third-Person Template Character

## Files Created
- `Source/MyProject/MyProjectCharacter.h`
- `Source/MyProject/MyProjectCharacter.cpp`

> Replace `MyProject` with your module name if it differs. The class name follows the default third-person template pattern (`<ProjectName>Character`), so it drops in without changing GameMode defaults.

## Architecture Rationale
- **Owner**: The player-controlled pawn remains the third-person template `ACharacter`, keeping the default camera boom + follow camera stack so the familiar template feel stays intact.
- **Responsibility**: This class owns input bindings (movement + a temporary TestLog action) and basic logging to prove the pawn and input are wired correctly in C++ only (no Blueprint dependency).
- **Dependency**: Uses `UCharacterMovementComponent` already on `ACharacter`; no extra components required for this step.

## C++ Code

### `MyProjectCharacter.h`
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MyProjectCharacter.generated.h"

/**
 * Default third-person template character adapted for the collect prototype.
 * Keeps the template camera boom/follow camera setup and adds a TestLog input for validation.
 */
UCLASS()
class MYPROJECT_API AMyProjectCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMyProjectCharacter();

protected:
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

private:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void HandleTestLog();
};
```

### `MyProjectCharacter.cpp`
```cpp
#include "MyProjectCharacter.h"

#include "GameFramework/Controller.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/InputComponent.h"

AMyProjectCharacter::AMyProjectCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    // Default third-person template tuning keeps the familiar feel.
    UCharacterMovementComponent* MoveComp = GetCharacterMovement();
    if (MoveComp)
    {
        MoveComp->MaxWalkSpeed = 600.f;
        MoveComp->BrakingDecelerationWalking = 2048.f;
    }

    // Third-person template camera stack.
    USpringArmComponent* SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->TargetArmLength = 300.f;
    SpringArm->bUsePawnControlRotation = true;

    UCameraComponent* FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;
}

void AMyProjectCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    check(PlayerInputComponent);

    // Third-person template axis names are kept so existing Project Settings mappings keep working.
    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &AMyProjectCharacter::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &AMyProjectCharacter::MoveRight);

    PlayerInputComponent->BindAction(TEXT("TestLog"), IE_Pressed, this, &AMyProjectCharacter::HandleTestLog);
}

void AMyProjectCharacter::MoveForward(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRot = Controller->GetControlRotation();
        const FRotator YawRot(0.f, ControlRot.Yaw, 0.f);

        const FVector Direction = FRotationMatrix(YawRot).GetUnitAxis(EAxis::X);
        AddMovementInput(Direction, Value);
    }
}

void AMyProjectCharacter::MoveRight(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRot = Controller->GetControlRotation();
        const FRotator YawRot(0.f, ControlRot.Yaw, 0.f);

        const FVector Direction = FRotationMatrix(YawRot).GetUnitAxis(EAxis::Y);
        AddMovementInput(Direction, Value);
    }
}

void AMyProjectCharacter::HandleTestLog()
{
    UE_LOG(LogTemp, Log, TEXT("TestLog input received on %s"), *GetName());
}
```

## Editor Setup (UE5)
1. Add the updated class files to your module, then compile.
2. In Project Settings → Input (the third-person template already has `MoveForward`/`MoveRight` axes):
   - Keep the existing axis mappings.
   - Add an **Action**: `TestLog` mapped to a convenient key (e.g., `T`).
3. GameMode defaults that pointed at the template character will continue to work because the class name matches (`<ProjectName>Character`). Only create a Blueprint subclass if you need to assign mesh/anim BP.
4. Play in PIE with the default third-person map to verify.

## Tests
- Play In Editor, move with configured keys; character should walk using Character Movement.
- Press the TestLog key; Output Log should print `TestLog input received on <PawnName>` confirming input binding.

## Fallbacks / Tips
- If movement axes do nothing, re-check Project Settings → Input axis names and key scales.
- If the log never appears, ensure the pawn is possessed (auto-possess or via GameMode) and that `TestLog` action name matches the binding exactly.
- If camera is missing, ensure SpringArm/Camera subobjects remain in the class or attach your own camera in a derived Blueprint.
