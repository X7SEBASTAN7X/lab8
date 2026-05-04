from __future__ import annotations
from math import sqrt
import random
from dataclasses import dataclass
import time

import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_COLOR = (20, 24, 30)
FPS = 60

# CUBE_COUNT = 20

CUBE_SIZE_COUNT: list[tuple] = [(5,25),(10,10),(30,4)]

CUBE_MIN_SIZE = 10
CUBE_MAX_SIZE = 75
CUBE_MIN_SPEED = 20
CUBE_MAX_SPEED = 200


#S
ANALYSIS_RADIUS = 100
ANALYSIS_RADIUS_SQ = ANALYSIS_RADIUS * ANALYSIS_RADIUS
FLEE_STEER = 1200

CHASE_STEER = 800

#Lifespan
LIFESPAN_MIN = 15
LIFESPAN_MAX = 60

#Random Bouncing
BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX = 95,105

RECT_CUBES: list = []


Color = tuple[int, int, int]



@dataclass
class Cube:
    x: float
    y: float
    size: int
    vx: float
    vy: float
    color: Color
    lifespan: float
    death: float


# Return a bright RGB color tuple so cubes contrast the dark background.
def random_color() -> Color:
    # Keep colors bright enough to stand out from the dark background.
    return (
        random.randint(70, 255),
        random.randint(70, 255),
        random.randint(70, 255),
    )


def create_random_cube(lifespan: float, size: int) -> Cube:
    # Shared spawn setup: choose size and position, pick a velocity
    # consistent with the size-based speed policy, and compute death time.
    x = random.uniform(0, WINDOW_WIDTH - size)
    y = random.uniform(0, WINDOW_HEIGHT - size)
    vx = random.choice((-1, 1)) * speed(size, CUBE_MIN_SPEED, CUBE_MAX_SPEED)
    vy = random.choice((-1, 1)) * speed(size, CUBE_MIN_SPEED, CUBE_MAX_SPEED)
    death = time.time() + lifespan
    return Cube(x=x, y=y, size=size, vx=vx, vy=vy, color=random_color(), lifespan=lifespan, death=death)


def create_cube(size: int = None) -> Cube:
    # Create a cube with a random lifespan within configured bounds.
    lifespan = random.randint(LIFESPAN_MIN, LIFESPAN_MAX)
    if size is None:
        size = random.randint(CUBE_MIN_SIZE, CUBE_MAX_SIZE) 
    return create_random_cube(lifespan, size=size)



def speed(size: int, mini: int, maxi: int) -> float:
    # Map size to a speed value: smaller cubes are faster. This uses
    # linear interpolation between `mini` and `maxi` based on size.
    return maxi - ((size - CUBE_MIN_SIZE) / (CUBE_MAX_SIZE - CUBE_MIN_SIZE)) * (maxi - mini)


def on_cube_bounce(cube: Cube, wall: str) -> None:
    """Stub hook: react to wall collisions (sound, score, effects, etc.)."""
    _ = (cube, wall)


def find_neighbors(cube: Cube, cubes: list[Cube], radius_sq: float)-> list[Cube]:
    # Find cubes whose center is within `radius_sq` of `cube` center.
    close = []
    # Squared-distance checks avoid sqrt() in this per-frame hot loop.
    cx, cy = cube.x + cube.size / 2, cube.y + cube.size / 2
    for neighbor in cubes:

        if neighbor is cube:
            continue
        nx, ny = neighbor.x + neighbor.size / 2, neighbor.y + neighbor.size / 2
        dx = cx - nx
        dy = cy - ny
        # Compare squared distance to avoid computing square roots.
        if dx * dx + dy * dy <= radius_sq:
            close.append(neighbor)
    return close


def compare_neighbors(cube: Cube, neighbors: list[Cube]) -> tuple[list[Cube], list[Cube]]:
    """Classify neighbors into threats (larger) and targets (smaller).

    A 'threat' is any neighbor strictly larger than `cube`; a 'target'
    is any neighbor strictly smaller. Equal-sized neighbors are ignored.
    """
    threats, targets = [], []
    for neighbor in neighbors:

        if neighbor.size > cube.size:
            threats.append(neighbor)
        elif neighbor.size < cube.size:
            targets.append(neighbor)
    return threats, targets


def single_target(targets: list[Cube])-> Cube | None:
    # Choose a single target (the smallest) to chase, or None.
    if not targets:
        return None
    smallest = targets[0]
    # Direct iteration is clearer for beginners than index-based loops.
    for candidate in targets[1:]:
        if candidate.size < smallest.size:
            smallest = candidate
    return smallest


def compute_chase_steering(cube: Cube, target: Cube, steer_strength: float) -> tuple[float, float]:
    # Compute a steering vector pointing from `cube` toward `target` and
    # scaled by `steer_strength`.
    if not target:
        return 0.0, 0.0

    cx, cy = cube.x + cube.size / 2, cube.y + cube.size / 2
    tx, ty = target.x + target.size / 2, target.y + target.size / 2

    dx, dy = tx - cx, ty - cy
    dist_sq = dx * dx + dy * dy

    if dist_sq > 0:
        # Reuse the computed length for normalization instead of recomputing.
        dist = sqrt(dist_sq)
        return (dx / dist) * steer_strength, (dy / dist) * steer_strength
    return 0.0, 0.0


def compute_flee_steering(cube: Cube, threats: list[Cube], steer_strength: float) -> tuple[float, float]:
    """Compute a steering vector that points away from nearby threats.

    For each threat we compute a unit vector pointing away, weight it by
    proximity (closer threats have higher weight), sum the contributions,
    normalize, and scale by `steer_strength`.
    """
    _ = (cube, threats, steer_strength)
    # Early-out when there are no threats.
    if not threats:
        return 0.0, 0.0

    steer_x, steer_y = 0.0, 0.0
    # Local copies make repeated values in this loop explicit and slightly cheaper.
    analysis_radius = ANALYSIS_RADIUS
    cx, cy = cube.x + cube.size / 2, cube.y + cube.size / 2

    # Accumulate weighted away vectors from each threat.
    for threat in threats:
        nx, ny = threat.x + threat.size / 2, threat.y + threat.size / 2
        dx, dy = cx - nx, cy - ny  # Vector from threat to cube
        dist_sq = dx * dx + dy * dy

        if dist_sq > 0:
            dist = sqrt(dist_sq)
            # Weight in [0,1) based on how close the threat is within analysis radius
            weight = (analysis_radius - dist) / analysis_radius
            steer_x += (dx / dist) * max(0.0, weight)
            steer_y += (dy / dist) * max(0.0, weight)

    # Normalize the combined vector and scale by steering strength.
    total_dist_sq = steer_x * steer_x + steer_y * steer_y
    if total_dist_sq > 0:
        total_dist = sqrt(total_dist_sq)
        return (steer_x / total_dist) * steer_strength, (steer_y / total_dist) * steer_strength

    return 0.0, 0.0


def apply_steering(cube: Cube, steer_x: float, steer_y: float, dt: float) -> None:
    """Apply steering to velocity while preserving the original speed magnitude.

    The function performs an Euler integration of the steering vector into
    velocity and then re-normalizes the velocity to the original speed so
    steering changes direction without changing the speed policy.
    """
    _ = (cube, steer_x, steer_y, dt)
    # No steering => nothing to do.
    if steer_x == 0 and steer_y == 0:
        return

    # Preserve the original speed magnitude so steering changes direction
    # without instantly speeding up or slowing down.
    orig_speed = sqrt(cube.vx**2 + cube.vy**2)

    # Integrate steering into velocity (simple Euler step)
    cube.vx += steer_x * dt
    cube.vy += steer_y * dt

    # Re-normalize velocity to original speed to enforce speed policy
    new_speed = sqrt(cube.vx**2 + cube.vy**2)
    if new_speed > 0:
        cube.vx = (cube.vx / new_speed) * orig_speed
        cube.vy = (cube.vy / new_speed) * orig_speed


def apply_bounce_damping(velocity: float) -> float:
    # Centralize repeated bounce math so damping policy lives in one place.
    damping = random.randint(BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX) / 100
    return -velocity * damping


def update_cube(cube: Cube, dt: float, cubes: list[Cube]) -> None:
    # Per-frame update for a single cubes
    # 1) Find neighbors and classify them as threats/targets. 
    neighbors = find_neighbors(cube, cubes, ANALYSIS_RADIUS_SQ)

    threats, targets = compare_neighbors(cube, neighbors)
    # Choose one target (smallest) to chase if any exist.
    target = single_target(targets)

    # 2) Compute steering: flee from threats, optionally chase a target.
    steer_x, steer_y = compute_flee_steering(cube, threats, FLEE_STEER)

    if target:
        chase_x, chase_y = compute_chase_steering(cube, target, CHASE_STEER)
        # Combine flee and chase vectors
        steer_x += chase_x
        steer_y += chase_y

    # 3) Apply steering to velocity while preserving overall speed.
    apply_steering(cube, steer_x, steer_y, dt)

    # 4) Integrate velocity into position.
    cube.x += cube.vx * dt
    cube.y += cube.vy * dt

    # 5) Handle wall collisions with simple position clamping and
    #    bounce damping so cubes reverse direction with a damping factor.
    # if cube.x <= 0:
    #     cube.x = 0
    #     cube.vx = apply_bounce_damping(cube.vx)
    #     on_cube_bounce(cube, "left")
    # elif cube.x + cube.size >= WINDOW_WIDTH:
    #     cube.x = WINDOW_WIDTH - cube.size
    #     cube.vx = apply_bounce_damping(cube.vx)
    #     on_cube_bounce(cube, "right")

    # if cube.y <= 0:
    #     cube.y = 0
    #     cube.vy = apply_bounce_damping(cube.vy)
    #     on_cube_bounce(cube, "top")
    # elif cube.y + cube.size >= WINDOW_HEIGHT:
    #     cube.y = WINDOW_HEIGHT - cube.size
    #     cube.vy = apply_bounce_damping(cube.vy)
    #     on_cube_bounce(cube, "bottom")

    # 5) New, Wrapping around:
    if cube.x <= 0:
        cube.x = WINDOW_WIDTH-cube.size
    elif cube.x + cube.size >= WINDOW_WIDTH:
        cube.x = 0+cube.size

    if cube.y <= 0:
        cube.y = WINDOW_HEIGHT-cube.size
    elif cube.y + cube.size >= WINDOW_HEIGHT:
        cube.y = 0+cube.size


def check_kill(to_kill: Cube)-> Cube:
    # Replace cube when its lifespan has elapsed by generating a new cube.
    ct = time.time()
    if to_kill.lifespan > 0 and ct > to_kill.death:
        to_kill = create_cube(to_kill.size)
    return to_kill


def draw_cube(surface: pygame.Surface, cube: Cube) -> None:
    # Draw cube as a circle for a softer visual than square rects.
    # (Original rect-based code is left as a comment for reference.)
    # rect = pygame.Rect(int(cube.x), int(cube.y), cube.size, cube.size)
    # pygame.draw.rect(surface, cube.color, rect, border_radius=4)
    # return rect

    # 1. Calculate the center point
    center_x = int(cube.x + cube.size / 2)
    center_y = int(cube.y + cube.size / 2)
    radius = int(cube.size / 2)
    pygame.draw.circle(surface, cube.color, (center_x, center_y), radius)
    

def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    cube_count: int,
    fps_value: float,
) -> None:
    # Render a small HUD with cube count and smoothed FPS value.
    message = f"Cubes: {cube_count}   FPS: {fps_value:.1f}   R: respawn   ESC: quit"
    text = font.render(message, True, (235, 238, 245))
    surface.blit(text, (14, 12))


def load_music(filename:str)->None:
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        print(f'File not found: {filename}')

def check_collision(cube: Cube, neighbor: Cube)-> bool:
    cx = int(cube.x + cube.size / 2)
    cy = int(cube.y + cube.size / 2)
    radius = int(cube.size / 2)
    if neighbor is Cube:
        nx, ny = neighbor.x + neighbor.size / 2, neighbor.y + neighbor.size / 2
        dx = cx - nx
        dy = cy - ny
        # Compare squared distance to avoid computing square roots.
        if dx * dx + dy * dy <= radius**2:
            return True
        return False
    return False


def main() -> None:
    # Initialize pygame and resources
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Cubes or Circles")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("couriernew", 20)
    load_music("overworld_day.mp3")

    # Create initial cube population
    cubes = [create_cube(size)  for number, size in CUBE_SIZE_COUNT
             for _ in range(number)]

    running = True
    displayed_fps = 0.0
    while running:
        # `dt` is the time delta in seconds used to make motion frame-rate independent
        dt = clock.tick(FPS)/1000
        current_fps = clock.get_fps()
        if current_fps > 0:
            # Smooth displayed FPS for a steadier readout
            displayed_fps = displayed_fps * 0.9 + current_fps * 0.1

        # Event handling: quit, toggle, and respawn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_r:
                    # Respawn a fresh set of cubes with new random properties
                    cubes = [create_cube(size)  for number, size in CUBE_SIZE_COUNT
                            for _ in range(number)]
        # Update each cube and replace it if its lifespan expired
        for i in range(len(cubes)):
            update_cube(cubes[i], dt, cubes)
            cubes[i]=check_kill(cubes[i])

        # Render pass: background, all cubes, HUD, then flip display
        screen.fill(BACKGROUND_COLOR)
        for i in range(len(cubes)):
            draw_cube(screen, cubes[i])

        draw_hud(screen, font, len(cubes), displayed_fps)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
