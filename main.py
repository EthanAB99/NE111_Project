#Samir Merchant, SM
#Ethan Batiuk, EB
#Keogan Larade, KL

"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice #importing the random choice that happens when a ghost hits the wall - SM
from turtle import * # importing graphics functions - KL

from freegames import floor, vector
import math


state = {'score': 0} #sets the original score to 0 when the game boots up - SM
path = Turtle(visible=False) # Sets the arrow checking what pelets were eaten to be invinvisible
writer = Turtle(visible=False) #Sets the arrow showing where the score is to invisible - SM
aim = vector(5, 0)
pacman = vector(-40, -80)#Where Pac-Man starts when the game boots-SM
clyde = [# Where the ghosts start when the game boots -SM
    [vector(100, -160), vector(-5, 0)],
]
blinky = [  
          [vector(-180, -160), vector(0, 5)],
]
pinky = [
          [vector(100, 160), vector(0, -5)],
]
inky = [
  [vector(-180, 160), vector(5, 0)],
]
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
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
#this is the game field, anywhere with a 1 is an allowed space, and anywhere with a 0 is a border you cannot cross.-EB

def square(x, y): # function for drawing the squares in the board - KL
    path.up() # these next four lines use the path variable which corresponds to the turtle import to draw the screen - KL
    path.goto(x, y) # ^ - KL
    path.down() # ^ - KL
    path.begin_fill() # ^ - KL

    for count in range(4): # chooses which squares to draw - KL
        path.forward(20) # dimensions of squares - KL
        path.left(90) # angle, making it a square - KL

    path.end_fill() # done drawing - KL


def offset(point):
    x = (floor(point.x, 20) + 200) / 20 # finds x coordinate of tile in which point lies - KL
    y = (180 - floor(point.y, 20)) / 20 # finds y coordinate of tile in which point lies - KL
    index = int(x + y * 20) # determines which tile the point lies in - KL
    return index # returns the value - KL


def valid(point):
    index = offset(point) # assigns the tile where the point lies to variable "index"  - KL
    if tiles[index] == 0: # checks if the tile is valid (playable, blue) - KL
      return False # if the tile is not valid/playable, false is returned - KL

    index = offset(point + 19) # checks if the point is valid anywhere in the tile (instead of just the origin of the tile) - KL

    if tiles[index] == 0: # checks if the tile is valid (playable, blue) - KL
        return False # if the tile is not valid/playable, false is returned - KL

    return point.x % 20 == 0 or point.y % 20 == 0 # returns True if the point is along the side of a tile, since the tiles are 20x20 pixel squares. 


def world():
    bgcolor('black') #setting the background colour-SM
    path.color('blue')#setting the path colour-SM

    for index in range(len(tiles)): #a for loop to set the bounds of the display of the game-SM
      
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200 # Where the game shows up in relation to screen - SM
            y = 180 - (index // 20) * 20# Where the game shows up in relation to screen - SM
            square(x, y)

          # when the nuber on the grid is one there is a dot that Pac-Man is able to collect-SM
            if tile == 1: 
                path.up()
                path.goto(x + 10, y + 10) #how many pixels away from the orgin the pelet is-SM
                path.dot(2, 'white') #The pixel size and color of the pelet-SM


def move():#the function that defines the movement and scoring aspect of the game. -EB
    writer.undo()
  #Makes it so that when you are changing direction, the last direction inputted becomes nothing so you can only move in the x or y direction not a combination of them both.-EB
    writer.write(state['score'])
  #tells python to display the score.-EB

    clear()
  #removes all elements from the list of vectors in the space.-EB

    if valid(pacman + aim):
        pacman.move(aim)
      #moves pacman across the grid if he is on a valid starting square, moves 5 pixels in the selected direction as defined earlier in the code.-EB

    index = offset(pacman)
  #defines what position Pacman is at for a specific moment on the grid.-EB

    if tiles[index] == 1:#calls onto the array of the grid and checks if the square is a 1.-EB
        tiles[index] = 2 #if it is it reassigns that specific value as a 2 and removes the power pellet from the board.-EB
        state['score'] += 1
      #This is for keeping score, as Pac-man moves across the grid and picks up pellets, the score increases by 1.-EB
        x = (index % 20) * 20 - 200#assigns a pixel value on the x-axis.-EB
        y = 180 - (index // 20) * 20#assgns a pixel value on the y-axis.-EB
        square(x, y)
      
      

    up()#imported turtle function that pulls the "pen" up which gives the character movement without a line behind it.-EB
    goto(pacman.x + 10, pacman.y + 10)#turtle function that essentially draws a line across the screen of where the character is moving, this helps make movement smoother rather than choppy
    dot(20, 'yellow')#graphics for pacman model.-EB

    for point, course in clyde:#for loop for when the ghosts hit a wall, it picks a new direction for it.-EB
      
        if valid(point + course):#checks if the point is valid and returns a boolean.-EB
            point.move(course)#if true, the ghost will move through the grid.-EB
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]#defines movement speed and direction for the ghosts
            plan = choice(options)#when a ghost hits a wall, it reads through options and picks a random but valid direction to move in so it does not try to go into walls but rather follows the path.
            course.x = plan.x #assigns an x value to point.move(course) 
            course.y = plan.y#assigns a y value to point.move(course)

        up()#lets the ghost move without a tracer behind it
        goto(point.x + 10, point.y + 10)#draws a path for the ghost to move along
        dot(20, 'red')#gives graphics to the ghosts as a red dot

#BREAK
    plant = vector(0, 5)
    for point, course in blinky:
        if valid(point + course):
          point.move(course)#Same as earlier; checks if blinky is moving on a valid square. -EB            
            
        else:
          options = [
              vector(5, 0),
              vector(-5, 0),
              vector(0, 5),
              vector(0, -5),
]#list of movement vectors in x and y directions
            
            
        
              
            #all the following lines check the position of pacman with respect to Blinky. if Blinky is below to to the right of pacman, he will try to move up or left. If one path is not allowed it will take the other. If neither is allowed it will go based on priority of; right, left, up down.If both paths are allowed it takes a point slightly above and slightly to the left and decides which point is closest to pacman then picks that path. We assign this direction to a variable plant and then add that to it's location which gives it motion. This goes on for all scenarios where pacman is below and to the right or straight down, etc. Because Blinky's grpahics are inside the if statements, he dissapears until he hits a wall.-EB/KL
          x = blinky[0][0].x
          y = blinky[0][0].y
          if pacman.x == blinky[0][0].x and pacman.y > blinky[0][0].y:
              if valid(point+options[2]):
                plant = options[2]
              else: 
                plant = choice(options)
          elif pacman.y == blinky[0][0].y and pacman.x > blinky[0][0].x:
            if valid(point+options[0]):
              plant = options[0]
            else: 
              plant = choice(options)
          elif pacman.x == blinky[0][0].x and pacman.y < blinky[0][0].y:
            if valid(point+options[3]):
              plant = options[3]
            else: 
              plant = choice(options)
          elif pacman.y == blinky[0][0].y and pacman.x < blinky[0][0].x:
            if valid(point+options[1]):
               plant = options[1]
            else: 
              plant = choice(options)
          elif pacman.x > blinky[0][0].x and pacman.y > blinky[0][0].y:
            if valid(point+options[0]) and not valid(point+options[2]):
              plant = (options[0])
            elif valid(point+options[2]) and not valid(point+options[0]):
              plant = (options[2])
            elif not valid(point+options[0]) and not valid(point+options[2]):
              plant = choice(options)
            elif valid(point+options[2]) and valid(point+options[0]):
              x = x+10
              y = y+10
              x= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              y= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              if x>=y:
                  p = 2              
                  plant = options[p]
              elif y>x:
                p = 0
                plant = options[p]
          elif pacman.x < blinky[0][0].x and pacman.y > blinky[0][0].y:
            if valid(point+options[2]) and not valid(point+options[1]):
              plant = (options[2])
            elif valid(point+options[1]) and not valid(point+options[2]):
              plant = (options[1])
            elif not valid(point+options[1]) and not valid(point+options[2]):
              plant = choice(options)
            elif valid(point+options[2]) and valid(point+options[1]):
              x = x-10
              y = y+10
              x= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              y= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              if x>=y:
                  p = 2
                  plant = options[p]
              elif y>x:
                  p = 1
                  plant = options[p]
          elif pacman.x < blinky[0][0].x and pacman.y < blinky[0][0].y:
            if valid(point+options[1]) and not valid(point+options[3]):
                plant = (options[1])
            elif valid(point+options[3]) and not valid(point+options[1]):
              plant = (options[3])
            elif not valid(point+options[1]) and not valid(point+options[3]):
              plant = choice(options)
            elif valid(point+options[1]) and valid(point+options[3]):
              x = x-10
              y = y-10
              x= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              y= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              if x>=y:
                  p = 3
                  plant = options[p]
                   
              elif y>x:
                  p = 1
                  plant = options[p]
          elif pacman.x > blinky[0][0].x and pacman.y < blinky[0][0].y:
            if valid(point+options[0]) and not valid(point+options[3]):
              plant = (options[0])
            elif valid(point+options[3]) and not valid(point+options[0]):
              plant = (options[3])
            elif not valid(point+options[0]) and not valid(point+options[3]):
              plant = choice(options)
            elif valid(point+options[0]) and valid(point+options[3]):
              x = x+10
              y = y-10
              x= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              y= math.sqrt((pacman.x - blinky[0][0].x)**2 + (pacman.y + blinky[0][0].y)**2)
              if x>=y:
                p = 3
                plant = options[p]
              elif y>x:
                p = 0
                plant = options[p]
                
          course.x = plant.x
          course.y = plant.y
          up()# Next three lines are graphics that give shape, size, color and removes the trail of blinky
          goto(blinky[0][0].x + 10,blinky[0][0].y + 10)
          dot(20,'orange')
          
#BREAK

    
    slant = vector(0, 5)
    for point, course in pinky:       
        if valid(point+course):
          point.move(course)#if last line is true, ghost will move along  set path. EB
          #Same as earlier; checks if pinky is moving on a valid square. -EB            
        else:   
            options = [
              vector(5, 0),
              vector(-5, 0),
              vector(0, 5),
              vector(0, -5),
            ]#list of movement vectors in x and y directions
          
          #all the following lines check the position of pacman with respect to Blinky. if Blinky is below to to the right of pacman, he will try to move up or left. If one path is not allowed it will take the other. If neither is allowed it will go based on priority of; right, left, up down.If both paths are allowed it takes a point slightly above and slightly to the left and decides which point is closest to pacman then picks that path. We assign this direction to a variable plant and then add that to it's location which gives it motion. This goes on for all scenarios where pacman is below and to the right or straight down, etc.-EB/KL
            x = pinky[0][0].x
            y = pinky[0][0].y
            if pacman.x == pinky[0][0].x and pacman.y > pinky[0][0].y:
                if valid(point+options[2]):
                  slant = options[2]
                else: 
                  slant = choice(options)
            elif pacman.y == pinky[0][0].y and pacman.x > pinky[0][0].x:
              if valid(point+options[0]):
                slant = options[0]
              else: 
                slant = choice(options)
            elif pacman.x == pinky[0][0].x and pacman.y < pinky[0][0].y:
              if valid(point+options[3]):
                slant = options[3]
              else: 
                slant = choice(options)
            elif pacman.y == pinky[0][0].y and pacman.x < pinky[0][0].x:
              if valid(point+options[1]):
                slant = options[1]
              else: 
                slant = choice(options)
            elif pacman.x > pinky[0][0].x and pacman.y > pinky[0][0].y:
              if valid(point+options[0]) and not valid(point+options[2]):
                slant = (options[0])
              elif valid(point+options[2]) and not valid(point+options[0]):
                slant = (options[2])
              elif not valid(point+options[0]) and not valid(point+options[2]):
                slant = choice(options)
              elif valid(point+options[2]) and valid(point+options[0]):
                x = x+10
                y = y+10
                x= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                y= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                if x>=y:
                    p = 2              
                    slant = options[p]
                elif y>x:
                  p = 0
                  slant = options[p]
            elif pacman.x < pinky[0][0].x and pacman.y > pinky[0][0].y:
              if valid(point+options[2]) and not valid(point+options[1]):
                slant = (options[2])
              elif valid(point+options[1]) and not valid(point+options[2]):
                slant = (options[1])
              elif not valid(point+options[1]) and not valid(point+options[2]):
                slant = choice(options)
              elif valid(point+options[2]) and valid(point+options[1]):
                x = x-10
                y = y+10
                x= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                y= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                if x>=y:
                    p = 2
                    slant = options[p]
                elif y>x:
                    p = 1
                    slant = options[p]
            elif pacman.x < pinky[0][0].x and pacman.y < pinky[0][0].y:
              if valid(point+options[1]) and not valid(point+options[3]):
                slant = (options[1])
              elif valid(point+options[3]) and not valid(point+options[1]):
                slant = (options[3])
              elif not valid(point+options[1]) and not valid(point+options[3]):
                slant = choice(options)
              elif valid(point+options[1]) and valid(point+options[3]):
                x = x-10
                y = y-10
                x= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                y= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                if x>=y:
                    p = 3
                    slant = options[p]
                   
                elif y>x:
                    p = 1
                    slant = options[p]
            elif pacman.x > pinky[0][0].x and pacman.y < pinky[0][0].y:
              if valid(point+options[0]) and not valid(point+options[3]):
                slant = (options[0])
              elif valid(point+options[3]) and not valid(point+options[0]):
                slant = (options[3])
              elif not valid(point+options[0]) and not valid(point+options[3]):
                slant = choice(options)
              elif valid(point+options[0]) and valid(point+options[3]):
                x = x+10
                y = y-10
                x= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                y= math.sqrt((pacman.x - pinky[0][0].x)**2 + (pacman.y + pinky[0][0].y)**2)
                if x>=y:
                  p = 3
                  slant = options[p]
                elif y>x:
                  p = 0
                  slant = options[p]
            course.x = slant.x
            course.y = slant.y
                
        up()# Next three lines are graphics that give shape, size, color and removes the trail of pinky
        goto(pinky[0][0].x + 10,pinky[0][0].y + 10)
        dot(20,'pink')

        gantt = vector(0, 5)
    for point, course in inky:
        if valid(point+course):
           point.move(course)
          #Same as earlier; checks if inky is moving on a valid square. -EB            
        elif (math.sqrt((pacman.x + inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2))>= 100:  #check ghost distance from pac-man 
            options = [
              vector(5, 0),
              vector(-5, 0),
              vector(0, 5),
              vector(0, -5),
            ]#list of movement vectors in x and y directions
            
            #if last line is true, ghost will move along  set path. EB
              
            #Inky is an interesting case, He will make his way towards pacman but only when he is farther than 100 pixels away, otherwise he will have a random movement pattern, sometimes waiting for his oppertunity to strike, making him the weirder of the ghosts.-EB/KL 
            x = inky[0][0].x
            y = inky[0][0].y
            if pacman.x == inky[0][0].x and pacman.y > inky[0][0].y:
                if valid(point+options[2]):
                  gantt = options[2]
                else: 
                  gantt = choice(options)
            elif pacman.y == inky[0][0].y and pacman.x > inky[0][0].x:
              if valid(point+options[0]):
                gantt = options[0]
              else: 
                gantt = choice(options)
            elif pacman.x == inky[0][0].x and pacman.y < inky[0][0].y:
              if valid(point+options[3]):
                gantt = options[3]
              else: 
                gantt = choice(options)
            elif pacman.y == inky[0][0].y and pacman.x < inky[0][0].x:
              if valid(point+options[1]):
                gantt = options[1]
              else: 
                gantt = choice(options)
            elif pacman.x > inky[0][0].x and pacman.y > inky[0][0].y:
              if valid(point+options[0]) and not valid(point+options[2]):
                gantt = (options[0])
              elif valid(point+options[2]) and not valid(point+options[0]):
                gantt = (options[2])
              elif not valid(point+options[0]) and not valid(point+options[2]):
                gantt = choice(options)
              elif valid(point+options[2]) and valid(point+options[0]):
                x = x+10
                y = y+10
                x= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                y= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                if x>=y:
                    p = 2              
                    gantt = options[p]
                elif y>x:
                  p = 0
                  gantt = options[p]
            elif pacman.x < inky[0][0].x and pacman.y > inky[0][0].y:
              if valid(point+options[2]) and not valid(point+options[1]):
                gantt = (options[2])
              elif valid(point+options[1]) and not valid(point+options[2]):
                gantt = (options[1])
              elif not valid(point+options[1]) and not valid(point+options[2]):
                gantt = choice(options)
              elif valid(point+options[2]) and valid(point+options[1]):
                x = x-10
                y = y+10
                x= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                y= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                if x>=y:
                    p = 2
                    gantt = options[p]
                elif y>x:
                    p = 1
                    gantt = options[p]
            elif pacman.x < inky[0][0].x and pacman.y < inky[0][0].y:
              if valid(point+options[1]) and not valid(point+options[3]):
                gantt = (options[1])
              elif valid(point+options[3]) and not valid(point+options[1]):
                gantt = (options[3])
              elif not valid(point+options[1]) and not valid(point+options[3]):
                gantt = choice(options)
              elif valid(point+options[1]) and valid(point+options[3]):
                x = x-10
                y = y-10
                x= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                y= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                if x>=y:
                    p = 3
                    gantt = options[p]
                   
                elif y>x:
                    p = 1
                    gantt = options[p]
            elif pacman.x > inky[0][0].x and pacman.y < inky[0][0].y:
              if valid(point+options[0]) and not valid(point+options[3]):
                gantt = (options[0])
              elif valid(point+options[3]) and not valid(point+options[0]):
                gantt = (options[3])
              elif not valid(point+options[0]) and not valid(point+options[3]):
                gantt = choice(options)
              elif valid(point+options[0]) and valid(point+options[3]):
                x = x+10
                y = y-10
                x= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                y= math.sqrt((pacman.x - inky[0][0].x)**2 + (pacman.y + inky[0][0].y)**2)
                if x>=y:
                  p = 3
                  gantt = options[p]
                elif y>x:
                  p = 0
                  gantt = options[p]
                
            course.x = gantt.x
            course.y = gantt.y
         
        up()# Next three lines are graphics that give shape, size, color and removes the trail of inky
        goto(inky[0][0].x + 10,inky[0][0].y + 10)
        dot(20,'purple')
  
    update()# updates the screen to show that the ghosts and pacman have moved otherwise we wouldn't be able to observe the changes.-EB
    die = False
    for point, course in clyde:#for loop for checking location of pacman compared to the clyde
        if abs(pacman - point) < 20:#if pacman is within a certain amount of pixels of the ghosts it acts like they are touching.-EB
          die = True
    for point, course in blinky:
        if abs(pacman - point) < 20:#checks if pacman is touching blinky, in which case the game ends
          die = True
          
    for point, course in pinky:
        if abs(pacman - point) < 20:#checks if pacman is touching pinky, in which case the game ends
          die = True

    for point, course in inky:
        if abs(pacman - point) < 20:#checks if pacman is touching inky, in which case the game ends
          die = True
          
    if die == True:#the line that ends the code
      return

    ontimer(move, 100)#recalls the move function after 100ms
    

    
  
def change(x, y): #how to know whether packman is able to move or not-SM
    if valid(pacman + vector(x, y)): #if able to move packman moves-SM
        aim.x = x
        aim.y = y
 # setup function is imported from turtle. it defines the size of the game display - KL

  
  
  
hideturtle() # imported from turtle, helps speed graphics up, hides an element turtle uses to help understand the graphics - KL
tracer(False) # imported from turtle, sets refresh rate of display - KL
writer.goto(160, 120) # imported from turtle, defines where the score is writen - KL
writer.color('white') # imported from turtle, defines colour of score - KL
writer.write(state['score']) # imported from turtle, displays the score - KL
listen() # imported from turtle, records any input - KL
onkey(lambda: change(5, 0), 'Right') #moves Pac-Man right 5 pixels -SM
onkey(lambda: change(-5, 0), 'Left') #moves Pac-Man left 5 pixels -SM 
onkey(lambda: change(0, 5), 'Up') #moves Pac-Man up 5 pixels -SM
onkey(lambda: change(0, -5), 'Down')#moves Pac-Man down 5 pixels -SM
world()#printing the gameplay screen - SM
move()
done()
