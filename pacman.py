from random import choice
from turtle import *
from base import floor, vector

state = {'score': 0}  #keep track of the score
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80) #starting position of pacman
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
#create the tiles for the pacman
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


def square(x, y):
    """
    Draw a square of size 20x20 at a specific position on the game grid.
    """
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill() #start drawing the square

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill() #finish drawing the square


def offset(point):
    """
    The function takes an input vector, and its purpose is to determine
    which tile in the tiles list corresponds to that specific point,
    based on the point's coordinates in the 2-D grid.
    Example: point = vector(-40, -80)
    x = (-40 + 200) / 20 = 8
    y = 180 - (-80) / 20 = 13
    Return value: (13 * 20) + 8 = 268 which corresponds to the 268th tile
    in the tiles list
    """
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """
    The function takes an input vector and determines whether the
    point lies on a valid path that the pacman can move on.
    """
    index = offset(point) #get the tile from the tiles list

    if tiles[index] == 0: #checks if the tile is a wall
        return False

    index = offset(point + 19) #check the edge of the 20x20 square to see if its a wall

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0 #ensure that the point is aligned with the grid of size 20x20


def world():
    """
    Draw the world grid on the screen where the blue tiles
    indicate a valid path that the pacman can move on and the
    black tiles indicates the path that the pacman can not move.
    """
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white') #create the food for pacman along the blue path


def move():
    """
    This function handles the movement of pacman and
    the ghosts, and updates the game state by checking
    for win or loss conditions by checking if the pacman
    collides with the ghosts
    """
    writer.undo()
    writer.write(state['score'])

    clear() #clear the current graphics

    if valid(pacman + aim): #check if the pacman next position is valid
        pacman.move(aim)

    index = offset(pacman)

    #check if the blue tile contains food and change the value of the tile if pacman eats the food on that tile
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y) #redraw the tile without the food

    up() #draw the pacman
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts: #loop through each ghosts position and direction
        if valid(point + course): #check if the next ghost position is valid
            point.move(course)
        else: #if the next position is invalid, select a random movement from the options list and update the ghost direction
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up() #draw the ghosts
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update() #update the screen to show all the features above

    for point, course in ghosts:
        if abs(pacman - point) < 20: #check if pacman is within 20 pixels of any ghost, which indicates collision
            return #end the game if pacman collides with a ghst

    ontimer(move, 100) #move function is called every 100ms for continuous movement of pacman and ghosts


def change(x, y):
    """
    Update the pacman's aim vector and control the direction
    pacman moves in the move function.
    """
    if valid(pacman + vector(x, y)): #add input direction to pacman's current position and check if the new position is valid
        aim.x = x #update x direction if the move is valid
        aim.y = y #update y direction if the move is valid


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
#event handling
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
