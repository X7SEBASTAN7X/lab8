from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = (20, 24, 30)
FPS = 60

CUBE_COUNT = 40
CUBE_MIN_SIZE = 20
CUBE_MAX_SIZE = 50
CUBE_MIN_SPEED = 50
CUBE_MAX_SPEED = 300

Color = tuple[int, int, int]


@dataclass
class Cube:
    x: float
    y: float
    size: int
    vx: float
    vy: float
    color: Color


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
    return Cube(x=x, y=y, size=size, vx=vx, vy=vy, color=random_color())


def customize_spawn(cube: Cube) -> Cube:
    """Stub hook: customize newly created cubes here."""
    return cube

def speed(size, mini, maxi):
    speed = 10000*(1/size)
    return speed if speed<=maxi else maxi

def on_cube_bounce(cube: Cube, wall: str) -> None:
    """Stub hook: react to wall collisions (sound, score, effects, etc.)."""
    _ = (cube, wall)


def update_cube(cube: Cube, dt: float) -> None:
    cube.x += cube.vx * dt
    cube.y += cube.vy * dt

    if cube.x <= 0:
        cube.x = 0
        cube.vx *= -1
        on_cube_bounce(cube, "left")
    elif cube.x + cube.size >= WINDOW_WIDTH:
        cube.x = WINDOW_WIDTH - cube.size
        cube.vx *= -1
        on_cube_bounce(cube, "right")

    if cube.y <= 0:
        cube.y = 0
        cube.vy *= -1
        on_cube_bounce(cube, "top")
    elif cube.y + cube.size >= WINDOW_HEIGHT:
        cube.y = WINDOW_HEIGHT - cube.size
        cube.vy *= -1
        on_cube_bounce(cube, "bottom")


def draw_cube(surface: pygame.Surface, cube: Cube) -> None:
    rect = pygame.Rect(int(cube.x), int(cube.y), cube.size, cube.size)
    pygame.draw.rect(surface, cube.color, rect, border_radius=4)


def draw_hud(surface: pygame.Surface, font: pygame.font.Font, cube_count: int) -> None:
    message = f"Cubes: {cube_count}   R: respawn   ESC: quit"
    text = font.render(message, True, (235, 238, 245))
    surface.blit(text, (14, 12))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Cubes (Stub Demo)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("couriernew", 20)

    cubes = [customize_spawn(create_cube()) for _ in range(CUBE_COUNT)]

    running = True
    while running:
        dt = clock.tick(FPS)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_r:
                    cubes = [customize_spawn(create_cube()) for _ in range(CUBE_COUNT)]

        for cube in cubes:
            update_cube(cube, dt)

        screen.fill(BACKGROUND_COLOR)
        for cube in cubes:
            draw_cube(screen, cube)
        draw_hud(screen, font, len(cubes))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()