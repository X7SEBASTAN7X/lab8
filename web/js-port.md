# JS Port Plan

## Goal
Port the current Pygame simulation in `main.py` into a single self-contained `index.html` file under `web/`, using only vanilla JavaScript, HTML5 Canvas, and standard browser APIs.

## Scope
- Primary source: `main.py`, because it is the executable entry point and contains the active simulation loop, rendering, input handling, and cube lifecycle.
- Reference source: `boids_exam.py` only if a later pass needs its boid-specific structure for comparison, but it is not the main target for this plan.
- Output target: one standalone `web/index.html` file with minimal CSS, a `<canvas>`, and one `<script>` block.
- Planning-only rule: do not implement any code yet; this document is the porting plan only.

## Structural Parity Rules
- Keep the logic 1-to-1 instead of refactoring it.
- Convert every Python class into a JavaScript class.
- Preserve function and variable meaning, translating snake_case names to camelCase only where JS style makes that necessary.
- Keep constants as constants and keep their roles unchanged.
- Map Python lists to JavaScript arrays and Python dictionaries to JavaScript objects.
- Preserve the same data flow and update order that `main.py` uses now.

## Source Inventory To Port
- `Cube` data model.
- Random cube creation helpers.
- Size-to-speed mapping helper.
- Neighbor search and collision logic.
- Chase and flee steering helpers.
- Velocity steering application.
- Bounce damping helper.
- Cube update, kill, respawn, and line trail logic.
- Drawing helpers for cubes, trails, and HUD.
- Main loop with event handling, update, render, and display flip behavior.

## HTML File Structure
- Minimal CSS to center the canvas and set the page background.
- A single `<canvas>` element sized to the simulation window.
- One `<script>` block that contains the full translated application.
- Brief JSDoc-style comments above the main class and loop sections explaining the Pygame equivalent.

## Translation Plan

### Data Model
- Port `Cube` as a JavaScript class with the same fields: position, size, velocity, color, lifespan, death time, and trail line.
- Store cube collections in arrays that mirror the Python list behavior.
- Keep color values as plain RGB tuples in Python terms, represented as arrays or small objects in JavaScript.

### Randomness And Setup
- Port `random_color`, `create_random_cube`, `create_cube`, and `speed` directly.
- Keep the same spawn bounds, lifespan range, size range, and speed scaling policy.
- Preserve the existing random sign choice for initial velocities.

### Neighbor And Collision Logic