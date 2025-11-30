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
