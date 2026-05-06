## EXERCISE 1 - Specific Amount and size
# 2pts
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
# 2pts
1. Make the kill function take the destroyed size and pass it on to the new create function

Implemented in line:280


## EXERCISE 3 - Screen Wrapping
# 2 pts
1. Instead of modifying direction, just reset the x or y by: 0 or the sreen size (adjusting by cube size to avoid bugs)

Commented old solution, new avalailable on lines:275-284

This implementation deprecates the following functions:
- apply_bounce_damping()
- on_cube_bounce()


## EXERCISE 4 - Collission detection
# 2 pts
- Decision: Copied the neighbor search and adjusted to what i think is correct
line:333
Had to redesign, might be wrong
checking dx * dx + dy * dy <= radius**2
with radius = int(neighbor.size / 2) + int(cube.size/2)
probably wrong but works

## EXERCISE 5 - Eating
# 3 pts
- Will try to implement this inside the neighbors function
Flow:
Is neighbor -> is target -> is colliding -> if true: Recreate

- Completed, but had to modify functions to additionally pass the cubes list as a total to know which cube needs to be replaced and being able to do it

## EXERCISE 6 - Eating ++
# 3 pts
Having lines when crossing the map

solved deleting the list when oging through

## EXERCISE 7 -  Trails
# 4 pts (maybe less)
Having lines when crossing the map

solved deleting the list when oging through


## Exercise 10
# 2 pts
Implemented correctly

## Exercise 11
# 2 pts
Implemented with
self.angle = random.uniform(self.angle-spread, self.angle+spread)

