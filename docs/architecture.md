# Project Architecture

## Scope
This architecture is derived from the current implementation in `main.py`.
The project is a single-module pygame simulation of autonomous moving entities (`Cube`).

## Module Dependency Graph
```mermaid
flowchart LR
    subgraph "Project Module"
        M["main.py"]
    end

    subgraph "External Library"
        P["pygame"]
    end

    subgraph "Python Standard Library"
        R["random"]
        T["time"]
        S["math.sqrt"]
        D["dataclasses.dataclass"]
        F["__future__.annotations"]
    end

    M -->|"imports"| P
    M -->|"imports"| R
    M -->|"imports"| T
    M -->|"imports"| S
    M -->|"imports"| D
    M -->|"imports"| F
```

## High-Level Runtime Flow
```mermaid
flowchart TD
    A["Program Start"] --> B["main"]
    B --> C["pygame.init() and display setup"]
    C --> D["load_music(overworld_day.mp3)"]
    D --> E["create initial cubes list"]
    E --> F{"running?"}

    F -->|"yes"| G["tick clock and compute dt/fps"]
    G --> H["process input events"]
    H --> I{"exit or respawn input?"}

    I -->|"exit"| Z["pygame.quit()"]
    I -->|"respawn"| E2["recreate cubes list"]
    E2 --> J["update every cube"]
    I -->|"continue"| J

    J --> K["render cubes and HUD"]
    K --> L["display.flip()"]
    L --> F

    F -->|"no"| Z
```

## Function-Level Call Graph
```mermaid
flowchart TB
    MAIN["main"] --> LM["load_music"]
    MAIN --> CC["create_cube"]
    MAIN --> UC["update_cube"]
    MAIN --> CK["check_kill"]
    MAIN --> DC["draw_cube"]
    MAIN --> DH["draw_hud"]

    CC --> SPD["speed"]
    CC --> RC["random_color"]

    UC --> FN["find_neighbors"]
    UC --> CN["compare_neighbors"]
    UC --> ST["single_target"]
    UC --> CFS["compute_flee_steering"]
    UC --> CCS["compute_chase_steering"]
    UC --> AS["apply_steering"]
    UC --> OCB["on_cube_bounce"]

    CK --> CC

    FN --> SQ1["sqrt"]
    CFS --> SQ2["sqrt"]
    CCS --> SQ3["sqrt"]
    AS --> SQ4["sqrt"]
```

## Primary Execution Sequence (Main Loop)
```mermaid
sequenceDiagram
    participant U as "User"
    participant E as "Event Queue"
    participant M as "main()"
    participant C as "Cube Update Pipeline"
    participant R as "Renderer"
    participant D as "Display"

    U->>E: "provides keyboard or window events"
    M->>M: "tick clock and smooth fps"
    M->>E: "poll pygame events"

    alt "quit event or ESC or Q"
        M->>M: "set running False"
    else "R key pressed"
        M->>M: "recreate cubes list"
    else "no control event"
        M->>M: "keep current cubes"
    end

    loop "for each cube index"
        M->>C: "update_cube(cube, dt, cubes)"
        C->>C: "neighbors, threats, target, steering"
        C->>C: "position update and wall bounce"
        C-->>M: "updated cube"
        M->>M: "check_kill and optional respawn"
    end

    loop "for each cube"
        M->>R: "draw_cube(surface, cube)"
    end

    M->>R: "draw_hud(surface, font, count, fps)"
    R->>D: "flip display"
```

## Key Architectural Notes
- Single-file architecture: all domain logic, rendering, and runtime orchestration are in `main.py`.
- Update pipeline is deterministic per frame order, but entity behavior is stochastic due to random initialization and bounce damping.
- Entity replacement strategy uses lifespan expiration (`check_kill`) to keep simulation population stable.
- Extension hooks exist (`on_cube_bounce`) for future side effects such as sound, score, or effects.
