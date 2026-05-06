# Porting Plan: boids_exam.py to JavaScript (HTML5 Canvas)

## 1. Goal
Port the existing Python/Pygame Boids simulation (`boids_exam.py`) into a single, standalone HTML file (`index.html`) using Vanilla JavaScript and HTML5 Canvas. The goal is strict structural parity.

## 2. Requirements

* **1-to-1 Mapping:** The Python logic must be preserved, preserving class, function, and variable names (converted to `camelCase`).
* **Data Structures:** Python Lists -> JS Arrays, Python Dicts -> JS Objects.
* **Game Loop:** Replace the `while running` and `clock.tick()` approach with `window.requestAnimationFrame()`. We will calculate the delta time (`dt`) manually to keep the speed consistent.
* **Graphics:** Translate `pygame.draw.polygon`, `screen.fill`, and font rendering to `CanvasRenderingContext2D` operations (`ctx.beginPath`, `ctx.moveTo`, `ctx.lineTo`, `ctx.fillStyle`, `ctx.fillText`, etc.).
* **Events:** Map Pygame event handling (`pygame.KEYDOWN`) to `window.addEventListener('keydown', ...)` events.

## 3. Structural Mapping

### Classes
* `Config` -> `class Config`
* `Boid` -> `class Boid`

### Boid Methods
* `__init__()` -> `constructor()`. Initialize `x`, `y`, `speed`, `vx`, `vy`.
* `_clampSpeed()` -> `_clampSpeed()`.
* `_screen_wrap()` -> `_screenWrap()`.
* `_screen_bounce()` -> `_screenBounce()`.
* `_random_steer(spread)` -> `_randomSteer(spread)`.
* `_separation(boids)` -> `_separation(boids)`.
* `_alignment(boids)` -> `_alignment(boids)`.
* `_cohesion(boids)` -> `_cohesion(boids)`.
* `update(boids, dt)` -> `update(boids, dt)`.
* `draw(screen)` -> `draw(ctx)`. Replaces `pygame.draw.polygon`.

### Functions
* `draw_hud(screen, font, config, fps)` -> `drawHud(ctx, config, fps)`.
* `run_simulation()` -> `runSimulation()`. Sets up canvas, event listeners, and starts the `requestAnimationFrame` loop.

## 4. Single-File Structure
The resulting `index.html` file will consist of:
1. `<html><head>...</head>` with a `<style>` block to center the canvas and apply a basic background color.
2. `<body>` containing `<canvas id="simulationCanvas"></canvas>`.
3. `<script>` tag containing the ported JS code implementing the behaviors listed above. Educational JSDoc comments will be included above major segments.

## 5. Next Steps
Once explicitly requested, this plan will be implemented in `web/index.html`.
