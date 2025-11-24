# Player Collect Mechanic — Step 1: Create `APlayerCharacter`

## Files Created
- `Source/MyProject/Player/PlayerCharacter.h`
- `Source/MyProject/Player/PlayerCharacter.cpp`

> Replace `MyProject` with your module name if it differs. Keep the folder path consistent inside the module (e.g., `Source/MyProject/Player/`).

## Architecture Rationale
- **Owner**: The player-controlled pawn should be an `ACharacter` to leverage the Character Movement Component for built-in walking, jumping, and navigation support.
- **Responsibility**: This class owns input bindings (movement + a temporary TestLog action) and basic logging to prove the pawn and input are wired correctly in C++ only (no Blueprint dependency).
- **Dependency**: Uses `UCharacterMovementComponent` already on `ACharacter`; no extra components required for this step.

## C++ Code

### `PlayerCharacter.h`
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PlayerCharacter.generated.h"

UCLASS()
class MYPROJECT_API APlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    APlayerCharacter();

protected:
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

private:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void HandleTestLog();
};
```

### `PlayerCharacter.cpp`
```cpp
#include "PlayerCharacter.h"
#include "GameFramework/Controller.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/InputComponent.h"

APlayerCharacter::APlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    // Optional: give the CharacterMovementComponent sane defaults.
    UCharacterMovementComponent* MoveComp = GetCharacterMovement();
    if (MoveComp)
    {
        MoveComp->MaxWalkSpeed = 600.f;
        MoveComp->BrakingDecelerationWalking = 2048.f;
    }

    // Optional camera boom + camera if you want a quick third-person view in PIE.
    USpringArmComponent* SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->TargetArmLength = 300.f;
    SpringArm->bUsePawnControlRotation = true;

    UCameraComponent* FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;
}

void APlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    check(PlayerInputComponent);

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &APlayerCharacter::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &APlayerCharacter::MoveRight);

    PlayerInputComponent->BindAction(TEXT("TestLog"), IE_Pressed, this, &APlayerCharacter::HandleTestLog);
}

void APlayerCharacter::MoveForward(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRot = Controller->GetControlRotation();
        const FRotator YawRot(0.f, ControlRot.Yaw, 0.f);

        const FVector Direction = FRotationMatrix(YawRot).GetUnitAxis(EAxis::X);
        AddMovementInput(Direction, Value);
    }
}

void APlayerCharacter::MoveRight(float Value)
{
    if (Controller && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRot = Controller->GetControlRotation();
        const FRotator YawRot(0.f, ControlRot.Yaw, 0.f);

        const FVector Direction = FRotationMatrix(YawRot).GetUnitAxis(EAxis::Y);
        AddMovementInput(Direction, Value);
    }
}

void APlayerCharacter::HandleTestLog()
{
    UE_LOG(LogTemp, Log, TEXT("TestLog input received on %s"), *GetName());
}
```

## Editor Setup (UE5)
1. Add the new class files to your module, then compile.
2. In Project Settings → Input:
   - **Axis**: `MoveForward` (W/S or Up/Down, Scale 1/-1), `MoveRight` (A/D or Left/Right, Scale -1/1).
   - **Action**: `TestLog` mapped to a convenient key (e.g., `T`).
3. Create a Blueprint subclass of `APlayerCharacter` only if you need to assign a skeletal mesh/anim BP; otherwise, set the C++ class directly in your GameMode’s default pawn.
4. Place the pawn in the level or ensure GameMode defaults spawn it.

## Tests
- Play In Editor, move with configured keys; character should walk using Character Movement.
- Press the TestLog key; Output Log should print `TestLog input received on <PawnName>` confirming input binding.

## Fallbacks / Tips
- If movement axes do nothing, re-check Project Settings → Input axis names and key scales.
- If the log never appears, ensure the pawn is possessed (auto-possess or via GameMode) and that `TestLog` action name matches the binding exactly.
- If camera is missing, ensure SpringArm/Camera subobjects remain in the class or attach your own camera in a derived Blueprint.
