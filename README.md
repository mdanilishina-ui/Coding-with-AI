# Coding-with-AI

This repository contains a UE5.6 Python scaffolding script that builds the C++ foundation for the **Coding_with_Ai** third-person prototype. Running the script inside the Unreal Editor writes the gameplay classes requested in the project brief: the renamed hero **AgentKai**, collectible items, an enemy AI controller, and a shader manager that reacts to distance and collection progress.

## How to use
1. Copy `Scripts/unreal_setup.py` into the root of your UE5 project (next to `Source/` and your `.uproject`).
2. In the Unreal Editor, open **Window → Developer Tools → Output Log** and run:
   ```python
   import Scripts.unreal_setup as setup
   setup.CodingWithAiSetup().run()
   ```
3. Build the project from the editor. The script produces:
   - `Coding_with_Ai.Build.cs`
   - Public/Private C++ classes for AgentKai, collectibles, enemy AI, and the progress shader manager
4. In your Third Person template level:
   - Set AgentKai as the default pawn and map the **Grab** action in Project Settings → Input.
   - Place `CollectibleItem` actors near the player start.
   - Drop an `EnemyAICharacter` and assign `EnemyAIController` as its AI Controller Class.
   - Add a `ProgressShaderManager` actor, assign your environment material to **BaseMaterial**, and set **PlayerActor**/**TargetActor** references.

Running the script repeatedly is safe; it overwrites the generated files so you can iterate on the C++ implementations as needed.

## How to test the first three collect-mechanic steps
1. **Run the setup script inside your UE5 project** following the steps above, then build the project so the generated C++ classes compile.
2. **Set AgentKai as the default pawn** in your GameMode.
3. **Bind inputs in Project Settings → Input**
   - Ensure the Third Person template axis mappings remain for `MoveForward`/`MoveRight`.
   - Add action mappings: `TestLog` (bind to a convenient key like `T`) and `Grab` (e.g., `E`).
4. **Place test actors in the level**
   - Drop a few `CollectibleItem` actors near the player start; assign a Static Mesh so they are visible.
   - Make sure AgentKai starts close enough to reach them.
5. **Step tests in PIE**
   - Press your `TestLog` key to confirm the character and inputs are wired; the Output Log should show `TestLog action pressed — input mapping confirmed.`
   - Look at the placed collectible to confirm it appears in the level (verifies the mesh-only pickup actor).
   - Stand within a couple meters of a collectible, aim at it, and press `Grab`; the Output Log should print `Grab trace hit: <ActorName>`, proving the sphere trace detects items.
