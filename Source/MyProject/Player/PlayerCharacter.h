#pragma once

#include "CoreMinimal.h"
#include "ThirdPersonCharacter.h"
#include "PlayerCharacter.generated.h"

/**
 * Backward-compatible player pawn that preserves the original PlayerCharacter naming
 * while reusing the updated ThirdPerson template-aligned setup.
 */
UCLASS()
class MYPROJECT_API APlayerCharacter : public AThirdPersonCharacter
{
    GENERATED_BODY()

public:
    APlayerCharacter();
};

