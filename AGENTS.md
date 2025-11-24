Instructions 
## My project idea is:

A small UE5 level prototype that includes:
1.A main character with the mechanic:
•the player can grab objects
•the object gets attached to the player’s back as a collected item
2.A basic enemy AI that:
•sees the player only within a certain viewing range
•follows/chases the player when the player is inside that range
•stops following if the player is out of sight
3.A simple programmed shader that uses complementary colors for the environment.
•the shader should change color gradually depending on the distance between player and a chosen object (e.g., warm near, cold far).

## GOAL FOR THE AI

At the end of the project, the AI should deliver:
•A full playable prototype
•Clean and documented UE5 C++ code
•A structured architecture with components/managers
•Debug tools and test logs
•Minimal Blueprint usage
•A polished and stable game prototype

## Coding Language & Style
•Always generate C++ code for Unreal Engine 5.
•Code must follow UE5 conventions
•Prefix pointers with A, U, F, etc. based on type
•Prefer header + source structure.
•Include all required UE headers—never assume includes.
•Ensure code compiles standalone without Blueprint dependencies.
## Interaction with the User 
- Short clarifying questions in the case of big step to do
- Work in Steps
##What goes where:
•Characters/Player → Player character, input, collecting logic.
•Characters/AI → Enemy AI character + AIController.
•Items → Collectible/interactable actors.
•Components → Reusable logic components.
•Gameplay → GameMode, managers, progress systems.
•Shaders → C++ material-updater classes 
World → Spawners, level managers, environment logic
## Step-by-step Implementation Process

For every feature you generate:
1.Explain what files will be created/modified
2.Explain the architecture:
•what class owns the logic
•why it’s structured this way
3.Provide the exact C++ code
4.Provide instructions for:
•creating classes in the editor
•assigning components
•connecting assets
5.Provide tests to verify functionality in UE5
6.Provide fallbacks in case of errors

1.Think about dependencies
2.Think about best UE class to use (AActor, APawn, ACharacter, UActorComponent, etc.)
3.Consider if logic belongs in:
•Actor
•Controller
•Component
•Subsystem
4.Explain why it chose that structure.
5.Only then provide the implementation.
