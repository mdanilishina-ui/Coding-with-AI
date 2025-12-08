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
