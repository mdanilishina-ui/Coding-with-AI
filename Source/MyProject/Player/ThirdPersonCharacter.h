#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ThirdPersonCharacter.generated.h"

class USpringArmComponent;
class UCameraComponent;

/**
 * Third-person character aligned with the UE template naming and setup.
 * Handles movement input and a temporary TestLog action for verification.
 */
UCLASS()
class MYPROJECT_API AThirdPersonCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AThirdPersonCharacter();

protected:
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

private:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    USpringArmComponent* CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    UCameraComponent* FollowCamera;

    void MoveForward(float Value);
    void MoveRight(float Value);
    void HandleTestLog();
};
