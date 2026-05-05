# Prompts History

Automatically captured prompt log. Entries are appended in chronological order (oldest first).

### 30-03-2026 12:57
- **Prompt**: read and setup the #file:journal-logger.agent.md

### 30-03-2026 13:55
- **Prompt**: make a small moving cubes using stubs and pygame

### 30-03-2026 14:02
- **Prompt**: can you make a venv and install pygame

### 30-03-2026 14:08
- **Prompt**: can you now undo everything you did to try and install it, i copied another venv called #.venv2 which works correctly

### 07-04-2026 09:51
- **Prompt**: Can you tell me if the speed function makes sense to make it faster or slower depending on the size of the cube?

### 07-04-2026 10:02
- **Prompt**: return maxi-(size-CUBE_MIN_SIZE/CUBE_MAX_SIZE-CUBE_MIN_SIZE)*(maxi-mini) so the better function could be this?
### 07-04-2026 11:27
- **Prompt**: I want to add so the smaller squares flee or change their trajectory from bigger squares. Do not five away the gull solution/algorithm, just help me learn how to do it progressively. Make sure to use function stubs and TODO
### 13-04-2026 14:13
- **Prompt**: #file:journal-logger.agent.md Reactivate the journal logger agent

### 13-04-2026 14:15
- **Prompt**: Generate the code explorer site for this project

### 13-04-2026 14:15
- **Prompt**: Analyze the Python project in /Users/seb1s/Documents/GitHub/lab8, specifically the main.py file. Generate a comprehensive code explorer site with:  1. Architecture diagrams (call graph, sequence diagrams, data flow) 2. Pattern analysis (3 good patterns, 2 potential issues) 3. Type hints analysis 4. Code review findings 5. Performance analysis if applicable 6. Next steps and resources  The project is a pygame-based simulation of moving cubes with steering/fleeing behavior. Focus on the key functions like: - find_bigger_neighbors: filtering logic - compute_flee_steering: avoidance algorithm - apply_steering: velocity adjustment - update_cube: main update loop  Output to /Users/seb1s/Documents/GitHub/lab8/docs/code_explorer.html

### 13-04-2026 14:24
- **Prompt**: Check and rebuild the website if/where broken

### 13-04-2026 14:29
- **Prompt**: im getting errors in the syntex error in text. mermaid version 11.14.0 Error rendering diagram. Error: Parse error on line 8: ...              m ->> loop: tick, handle e -----------------------^ Expecting '+', '-', '()', 'ACTOR', got 'loop'  Source:                  sequenceDiagram                     participant m as main                     participant loop as "Event Loop"                     participant upd as update_cube                     participant drw as draw_cube                     participant pygame_d as "Pygame Display"                                          m ->> loop: tick, handle events                     loop ->> upd: for each cube                     upd -->> loop: cube updated                     loop ->> drw: for each cube                     drw -->> loop: drawn                     loop ->> pygame_d: flip display

### 20-04-2026 10:33
- **Prompt**: @file:code-explorer.agent.md read the #file:code_explorer.html  make a new version of code explorer with the date in the name

### 20-04-2026 10:36
- **Prompt**: 🔴 Dead Code & Inconsistency The in_radius() function duplicates distance logic but is never called. Also, velocity is randomly scaled (0.95–1.05) on bounce, causing subtle speed drift over time.  Basics: in_radius() calculates distance but isn't imported or called anywhere. The random bounce factor might be unintended. Engineering: Dead code accumulates technical debt. The random bounce factor is poorly documented—is it intentional for realism, or a bug? Unclear intent slows debugging. Architecture: Either remove in_radius() or refactor to use it (DRY principle). Document the random bounce with a comment explaining the game design rationale.  You say this, can you explain

### 20-04-2026 10:39
- **Prompt**: @file:code-explorer.agentread the #file:code_explorer.html make a new version of code explorer with the date in the name

### 20-04-2026 10:40
- **Prompt**: @file:code-explorer.agent.md  read the #file:code-explorer-template.html and modify and update the #file:code_explorer_2026-04-20.html accordingly to the code

### 20-04-2026 10:41
- **Prompt**: @file:code-explorer.agent.md read the #file:code_explorer.html  make a new version of code explorer with the date in the name

### 20-04-2026 11:03
- **Prompt**: @file:code-explorer.agent.md read the #file:code_explorer.html  make a v2 of todays version

### 20-04-2026 11:08
- **Prompt**: yes, refresh the content and upgrade the diagram

### 20-04-2026 11:13
- **Prompt**: check for any mistakes and DONT append this to the journal

### 20-04-2026 11:20
- **Prompt**: check and correct this file according to the @file:code-explorer.agent.md  and the #file:code-explorer-template.html

### 21-04-2026 09:27
- **Prompt**: Regenerate the code explorer reading my code and make sure to put the date on the filename

### 21-04-2026 09:42
- **Prompt**: can you give me which statemets are affected by this and is there a more efficient way to make it  from math import *

### 21-04-2026 09:42
- **Prompt**: and what about using **1/2

### 21-04-2026 09:44
- **Prompt**: Regenerate code explorer with #file:code-explorer-template.html with the new updates on #file:main.py

### 27-04-2026 13:41
- **Prompt**: @file:code-explorer.agent.md generate a #file:code-explorer-template.html with the latest stuff in #file:main.py and put it on code_explorer and todays date

### 27-04-2026 13:42
- **Prompt**: Analyze /Users/seb1s/Documents/GitHub/lab8/main.py and generate an updated code explorer HTML using /Users/seb1s/Documents/GitHub/lab8/.github/agents/code-explorer-template.html as the blueprint. Fill all slots with current analysis from main.py, include required diagrams and sections, and write to /Users/seb1s/Documents/GitHub/lab8/docs/code_explorer.html. Then also create/update a dated copy at /Users/seb1s/Documents/GitHub/lab8/docs/code_explorer_2026-04-27.html with identical content. Ensure Mermaid diagram IDs are safe/opaque and rendering uses the template JS conventions. Do not modify main.py.

### 27-04-2026 14:14
- **Prompt**: activate the architecture-graphs agent

### 27-04-2026 14:17
- **Prompt**: @file:architecture-graphs.agent.md generate the architecture documents for this project

### 27-04-2026 14:17
- **Prompt**: generate the architerture documents for this projects

### 27-04-2026 14:21
- **Prompt**: High-Level Runtime Flow Syntax error in text mermaid version 11.14.0 Core frame loop branches on quit and respawn controls, then updates and renders.

### 27-04-2026 14:24
- **Prompt**: do the flash quiz site twin

### 27-04-2026 14:40
- **Prompt**: Give me a refactoring plan to make it more efficient

### 27-04-2026 14:50
- **Prompt**: Implement the refactoring into the #file:main.py

### 04-05-2026 09:41
- **Prompt**: add comments to explain each logic step and function. and dont change anything

### 05-05-2026 13:43
- **Prompt**: check #file:MY_EXAM.md and #file:main.py and list problems in logic that match the implementations listed in #file:MY_EXAM.md

### 05-05-2026 14:28
- **Prompt**: /create-agent  Transpiler Agent - Prompt Role: You are a Senior Software Engineer helping Computer Science students understand cross-language porting. Goal: Prepare a plan to port the attached Python/Pygame application into a single, standalone index.html file using Vanilla JavaScript and HTML5 Canvas. The final results will be located in a local ‘web’ directory. The plan itself should also be located in the ‘web’ directory. Write this plan to js-port.md. Do not start implementing it until I explicitly ask you to do so later. Requirements for Structural Parity: 1-to-1 Mapping: Do not "refactor" the logic. Every Python Class must become a JavaScript Class. Every Function and Variable name should remain identical (translated to camelCase where appropriate for JS convention). Do not try to fix bugs or improve  or refactor the code. Data Structures: Map Python Lists to JS Arrays and Python Dictionaries to JS Objects. Maintain the same data flow used in the main.py. The Simulation Loop: > - Replace the pygame event loop and while loop with a requestAnimationFrame() loop. Implement the dt (delta time) calculation logic to ensure the simulation speed matches the original Python clock.tick() behavior. Graphics: Use the native CanvasRenderingContext2D (ctx) for all drawing. Map pygame.draw methods (rect, circle, etc.) to the equivalent ctx methods. Input/Events: If there are mouse or keyboard interactions, map pygame.event listeners to standard JS addEventListener calls. Self-Contained File: Provide the final code as one complete index.html file containing: Minimal CSS to center the canvas and set a background color. The <canvas> element. The <script> block containing the ported logic. Educational Documentation: > Within the code, add brief JSDoc comments above the main classes or loops explaining what the Pygame equivalent was (e.g., "// Equivalent to pygame.display.flip()").

