## EXERCISE 1 - Specific Amount and size

1. Create new Variable containing amount of cubes to create and its size:
list[tuple] 
line:16

2. Modify function "create_cube" and "create_random_cube" to accept size, and if size not given make it random.
lines:64-80

3. Apply changes on creating to unpack values
line:327
line:349

- Additional: Changed unpacking to amount, size. Because i had it on the wrong order

## EXERCISE 2 - Respawn with same size

1. Make the kill function take the destroyed size and pass it on to the new create function

Implemented in line:280


## EXERCISE 3 - Screen Wrapping

1. Instead of modifying direction, just reset the x or y by: 0 or the sreen size (adjusting by cube size to avoid bugs)

Commented old solution, new avalailable on lines:275-284

This implementation deprecates the following functions:
- apply_bounce_damping()
- on_cube_bounce()


## EXERCISE 4 - Collission detection
- Decision: Copied the neighbor search and adjusted to what i think is correct
line:333