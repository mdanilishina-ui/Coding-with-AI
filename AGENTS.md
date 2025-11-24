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

##Workflow
STEP 1 — AI creates the Player Character class
AI creates APlayerCharacter with basic movement and one test input that logs a message.
Test: Player can move in PIE and pressing the test key prints a log.

STEP 2 — AI creates a basic CollectibleItem actor
AI generates ACollectibleItem with a static mesh component only.
Test: Item appears correctly when placed in the level.

STEP 3 — AI adds SphereTrace detection to the player
AI implements a sphere trace fired on the Grab key press.
Test: Standing near an item and pressing Grab prints the hit actor name.

STEP 4 — AI implements pickup logic
AI adds a collected-items array and removes the item from the world when grabbed.
Test: Pressing Grab removes the item and logs “Item collected”.

STEP 5 — AI attaches collected items to the player’s back
AI replaces destroy-with-attach logic and attaches items to sequential back sockets.
Test: Collected items appear attached on the player’s back.

STEP 6 — AI creates an enemy character and AI controller
AI creates AEnemyAICharacter and AEnemyAIController and hooks them together.
Test: Placing the enemy in the world prints a log confirming the AI started.

STEP 7 — AI adds sight perception to the enemy AI
AI adds UAIPerceptionComponent with a sight sense to detect the player.
Test: Walking into the AI’s vision prints “Player seen!”; leaving prints “Player lost!”.

STEP 8 — AI implements chase behavior
AI makes the enemy use MoveToLocation to follow the player when seen.
Test: AI chases the player when visible and stops when hidden.

STEP 9 — AI implements search behavior
AI adds a 60-second search mode: move to last known player location and check random points.
Test: Losing the AI’s sight triggers realistic search movement for one minute.

STEP 10 — AI creates a shader controller
AI builds AProgressShaderManager that creates a dynamic material instance and updates a float parameter (HeatValue).
Test: Material changes visually when HeatValue is modified.

STEP 11 — AI implements distance-based heat/cold logic
AI updates HeatValue every Tick based on distance between player and target.
Test: Approaching the target warms the color; walking away cools it.

STEP 12 — AI creates a progress system
AI tracks number of items collected and maps progress to shader intensity.
Test: Collecting more items gradually increases heat/brightness of the shader effect.

STEP 13 — AI performs integration cleanup
AI removes unnecessary Tick functions, adds pointer safety, adds debug logs, and verifies component ownership.
Test: All systems run without warnings, crashes, or unexpected behavior.

STEP 14 — AI performs optional polish
AI adds small improvements like smoother item attach animation, better debug visuals, or optional AI tweaks.
Test: Prototype behaves smoothly and feels polished.

## Testable To-Do Steps by Mechanic

**Player Collect Mechanic**
1. Create `APlayerCharacter` with movement input and a temporary “TestLog” input action that prints to log in PIE (confirms class + input setup).
2. Add `ACollectibleItem` actor containing only a Static Mesh component; drop it in the level to verify visibility/spawn.
3. Implement a Grab key SphereTrace from the player; in PIE, standing near an item and pressing Grab should print the hit actor name (proves detection).
4. On successful trace, push the item into a collected-items array and remove it from the world; test by pressing Grab to see “Item collected” and item disappearance.
5. Swap removal for attaching: when grabbed, attach the item to sequential back sockets on the player; test visually that items line up on the back after multiple pickups.

**Enemy Vision & Pursuit**
1. Create `AEnemyAICharacter` and `AEnemyAIController`, ensure the pawn uses the controller; place in level and confirm startup log fires (verifies possession/setup).
2. Add `UAIPerceptionComponent` with sight sense tuned to desired range; walking into view should log “Player seen!”, leaving should log “Player lost!” (validates sensing).
3. On “seen,” call `MoveToLocation` toward the player; confirm the AI moves while player visible and halts when hidden (chase loop works).
4. When sight is lost, enter a 60-second search: move to last known player location, then probe random points; verify the timed search behavior triggers on loss of sight.

**Shader Distance Feedback**
1. Implement `AProgressShaderManager` that creates a Dynamic Material Instance and updates a `HeatValue` scalar; manually tweak the value in PIE to see material color change (proves binding).
2. Tick: compute distance between player and target actor, map it to `HeatValue`; test by walking closer/farther to observe warm→cool transitions.
3. Hook collected-item count into the shader manager to scale intensity/brightness; collect multiple items and verify the visual effect ramps with progress.

**Stability & Polish**
1. Integration pass: remove unnecessary Ticks, add null checks/pointer safety, and ensure ownership is correct; run the prototype to confirm no warnings or crashes (baseline stability).
2. Optional polish: add smoother attach animations, clearer debug visuals, or minor AI tuning; validate visually/behaviorally that the prototype feels smoother.
