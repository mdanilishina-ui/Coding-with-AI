#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PlayerCharacter.generated.h"

UCLASS()
class YOURPROJECT_API APlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    APlayerCharacter();

protected:
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    void MoveForward(float Value);
    void MoveRight(float Value);
    void HandleTestLog();

    UPROPERTY(VisibleAnywhere)
    class USpringArmComponent* CameraBoom;

    UPROPERTY(VisibleAnywhere)
    class UCameraComponent* FollowCamera;
};
