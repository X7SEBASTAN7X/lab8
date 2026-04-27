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

CUBE_COUNT = 20
CUBE_MIN_SIZE = 10
CUBE_MAX_SIZE = 75
CUBE_MIN_SPEED = 20
CUBE_MAX_SPEED = 200


#S
ANALYSIS_RADIUS = 100
FLEE_STEER = 1200

CHASE_STEER = 800

#Lifespan
LIFESPAN_MIN = 15
LIFESPAN_MAX = 60

#Random Bouncing
BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX = 95,105

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

def random_color() -> Color:
    # Keep colors bright enough to stand out from the dark background.
    return (
        random.randint(70, 255),
        random.randint(70, 255),
        random.randint(70, 255),
    )

def create_cube() -> Cube:
    size = random.randint(CUBE_MIN_SIZE, CUBE_MAX_SIZE)
    x = random.uniform(0, WINDOW_WIDTH - size)
    y = random.uniform(0, WINDOW_HEIGHT - size)
    vx = random.choice((-1, 1)) * speed(size, CUBE_MIN_SPEED, CUBE_MAX_SPEED)
    vy = random.choice((-1, 1)) * speed(size, CUBE_MIN_SPEED, CUBE_MAX_SPEED)
    lifespan = random.randint(LIFESPAN_MIN,LIFESPAN_MAX)
    death = time.time() + lifespan
    return Cube(x=x, y=y, size=size, vx=vx, vy=vy, color=random_color(), lifespan=lifespan,death=death)

def create_player() -> Cube:
    size = random.randint(CUBE_MIN_SIZE, CUBE_MAX_SIZE)
    x = random.uniform(0, WINDOW_WIDTH - size)
    y = random.uniform(0, WINDOW_HEIGHT - size)
    vx = random.choice((-1, 1)) * speed(size, CUBE_MIN_SPEED, CUBE_MAX_SPEED)
    vy = random.choice((-1, 1)) * speed(size, CUBE_MIN_SPEED, CUBE_MAX_SPEED)
    lifespan = 4096 
    death = time.time() + lifespan
    return Cube(x=x, y=y, size=size, vx=vx, vy=vy, color=random_color(), lifespan=lifespan,death=death)


def customize_spawn(cube: Cube) -> Cube:
    """Stub hook: customize newly created cubes here."""
    return cube

def speed(size: int, mini: int, maxi: int) -> float:
    return maxi - ((size - CUBE_MIN_SIZE) / (CUBE_MAX_SIZE - CUBE_MIN_SIZE)) * (maxi - mini)

def on_cube_bounce(cube: Cube, wall: str) -> None:
    """Stub hook: react to wall collisions (sound, score, effects, etc.)."""
    _ = (cube, wall)

def find_neighbors(cube: Cube, cubes: list[Cube], radius: float)-> list[Cube]:
    close = []
    cx, cy = cube.x + cube.size / 2, cube.y + cube.size / 2
    for neighbor in cubes:
        if neighbor is cube:
            continue
        nx, ny = neighbor.x + neighbor.size / 2, neighbor.y + neighbor.size / 2
        dist = sqrt((cx - nx)**2 + (cy - ny)**2)
        if dist <= radius:
            close.append(neighbor)
    return close

def compare_neighbors(cube: Cube, neighbors: list[Cube]) -> tuple[list[Cube], list[Cube]]:
    """Stub: return bigger cubes near the current cube."""
    threats, targets = [], []
    for neighbor in neighbors:
        if neighbor.size > cube.size:
            threats.append(neighbor)
        elif neighbor.size < cube.size:
            targets.append(neighbor)
    return threats, targets

def single_target(targets: list[Cube])-> Cube | None:
    if not targets:
        return None
    smallest = targets[0]
    for i in range(len(targets)):
        if targets[i].size<smallest.size:
            smallest=targets[i]
    return smallest

def compute_chase_steering(cube: Cube, target: Cube, steer_strength: float) -> tuple[float, float]:
    if not target:
        return 0.0, 0.0

    cx, cy = cube.x + cube.size / 2, cube.y + cube.size / 2
    tx, ty = target.x + target.size / 2, target.y + target.size / 2

    dx, dy = tx - cx, ty - cy
    dist = sqrt(dx**2 + dy**2)
    
    if dist > 0:
        return (dx / dist) * steer_strength, (dy / dist) * steer_strength
    return 0.0, 0.0

def compute_flee_steering(cube: Cube, threats: list[Cube], steer_strength: float) -> tuple[float, float]:
    """Stub: compute steering vector that points away from nearby threats."""
    _ = (cube, threats, steer_strength)
    #Step 2: build an "away" direction for each threat and combine them.
    # Step 2: scale the final vector by steer_strength.
    if not threats:
        return 0.0, 0.0

    steer_x, steer_y = 0.0, 0.0
    cx, cy = cube.x + cube.size / 2, cube.y + cube.size / 2

    for threat in threats:
        nx, ny = threat.x + threat.size / 2, threat.y + threat.size / 2
        
        dx, dy = cx - nx, cy - ny # Get a vector between the cube and the threat
        dist = sqrt(dx**2 + dy**2)
        
        if dist > 0:
            weight = (ANALYSIS_RADIUS - dist) / ANALYSIS_RADIUS # To now how urgent it is
            steer_x += (dx / dist) * max(0.0, weight) 
            steer_y += (dy / dist) * max(0.0, weight) 

    total_dist = sqrt(steer_x**2 + steer_y**2)
    if total_dist>0:
    # Normalize and multiply by the strength to make it look more or less intentional
        return (steer_x / total_dist ) * steer_strength, (steer_y / total_dist) * steer_strength
    
    return 0.0, 0.0


def apply_steering(cube: Cube, steer_x: float, steer_y: float, dt: float) -> None:
    """Stub: apply steering to velocity while preserving your speed policy."""
    _ = (cube, steer_x, steer_y, dt)
    # Step 3: add steering to cube.vx / cube.vy.
    # Step 3: clamp resulting speed if needed.
    if steer_x == 0 and steer_y == 0:
        return

    orig_speed = sqrt(cube.vx**2 + cube.vy**2)
    
    cube.vx += steer_x * dt
    cube.vy += steer_y * dt
    
    new_speed = sqrt(cube.vx**2 + cube.vy**2)
    if new_speed > 0:
        cube.vx = (cube.vx / new_speed) * orig_speed
        cube.vy = (cube.vy / new_speed) * orig_speed


def update_cube(cube: Cube, dt: float, cubes: list[Cube]) -> None:
    #Make it flee
    neighbors = find_neighbors(cube, cubes, ANALYSIS_RADIUS)

    threats, targets = compare_neighbors(cube, neighbors)
    target = single_target(targets)

    steer_x, steer_y = compute_flee_steering(cube, threats, FLEE_STEER)

    if target:
        chase_x, chase_y = compute_chase_steering(cube, target, CHASE_STEER)
        
        steer_x += chase_x
        steer_y += chase_y

    apply_steering(cube, steer_x, steer_y, dt)

    cube.x += cube.vx * dt
    cube.y += cube.vy * dt

    if cube.x <= 0:
        cube.x = 0
        cube.vx *= -1
        cube.vx *= random.randint(BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX)/100
        on_cube_bounce(cube, "left")
    elif cube.x + cube.size >= WINDOW_WIDTH:
        cube.x = WINDOW_WIDTH - cube.size
        cube.vx *= -1
        cube.vx *= random.randint(BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX)/100
        on_cube_bounce(cube, "right")

    if cube.y <= 0:
        cube.y = 0
        cube.vy *= -1
        on_cube_bounce(cube, "top")
        cube.vy *= random.randint(BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX)/100
    elif cube.y + cube.size >= WINDOW_HEIGHT:
        cube.y = WINDOW_HEIGHT - cube.size
        cube.vy *= -1
        cube.vy *= random.randint(BOUNCE_DAMPING_MIN, BOUNCE_DAMPING_MAX)/100
        on_cube_bounce(cube, "bottom")


def check_kill(to_kill: Cube)-> Cube:
    # If it has a to die its an int so true
    # and if it has to be killed.
    ct = time.time()
    if to_kill.lifespan and ct>to_kill.death:
        to_kill = create_cube()
    return to_kill


def draw_cube(surface: pygame.Surface, cube: Cube) -> None:
    # rect = pygame.Rect(int(cube.x), int(cube.y), cube.size, cube.size)
    # pygame.draw.rect(surface, cube.color, rect, border_radius=4)

    #Alternative to make circles instead of squares

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
    message = f"Cubes: {cube_count}   FPS: {fps_value:.1f}   R: respawn   ESC: quit"
    text = font.render(message, True, (235, 238, 245))
    surface.blit(text, (14, 12))

def load_music(filename:str)->None:
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        print(f'File not found: {filename}')

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Cubes or Circles")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("couriernew", 20)
    load_music("overworld_day.mp3")

    cubes = [customize_spawn(create_cube()) for _ in range(CUBE_COUNT)]

    running = True
    displayed_fps = 0.0
    while running:
        dt = clock.tick(FPS)/1000
        current_fps = clock.get_fps()
        if current_fps > 0:
            displayed_fps = displayed_fps * 0.9 + current_fps * 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_r:
                    cubes = [customize_spawn(create_cube()) for _ in range(CUBE_COUNT)]

        for i in range(len(cubes)):
            update_cube(cubes[i], dt, cubes)
            cubes[i]=check_kill(cubes[i])

        screen.fill(BACKGROUND_COLOR)
        for cube in cubes:
            draw_cube(screen, cube)
        draw_hud(screen, font, len(cubes), displayed_fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()