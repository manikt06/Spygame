import turtle
import random
import winsound
import time
import pygame

turtle.speed(0)
turtle.bgcolor("blue")
#image background
turtle.bgpic("spacewarbg.png")
turtle.title("MT SPACE")
# ht=hide turtle
turtle.ht()
# reduces the memory=.setundobuffer
turtle.setundobuffer(1)
# tracer=speed up the animation
turtle.tracer(0)#tracer tell how many times screen gets updated
# sprite = objects on the screen!!
# turtle.Turtle(inherits everything of turtle module)
#_____________________________________________________________________________________________________________________
class sprite(turtle.Turtle):
    def __init__(self , spriteshape , color , startx , starty):
        turtle.Turtle.__init__(self,shape=spriteshape)#child class
        # speed of animation(0=fastest)
        self.speed(0)
        self.penup()
        self.color(color)
        # fd= forward
        self.fd(0)
        self.goto(startx,starty)
        # here speed= speed of the player object:
        self.speed = 3
        # method for movement
    def move(self):
        self.fd(self.speed)

# _____________________________________________________________________________________________________________________
# boundary detection(cannot cross the boundary):
        if self.xcor() > 290:
            self.setx(290)#so it doesnot cross the border
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
#_____________________________________________________________________________________________________________________
#    if player collides with enemy:(collison)#
#    self = player , other = enemies
    def is_collision(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False
#______________________________________________________________________________________________________________________
# player
class player(sprite):
    def __init__(self,spriteshape,color,startx,starty):
        sprite.__init__(self,spriteshape,color,startx,starty)
        self.shapesize(stretch_wid=0.5,stretch_len=1.1)
        self.speed =4
# movement in left,right direction:
    def turn_left(self):
        self.lt(45)
    def turn_right(self):
        self.rt(45)
    def accelerate(self):
        self.speed +=1
    def deaccelerate(self):
        self.speed -=1
#______________________________________________________________________________________________________________________
#enemy
class enemy(sprite):
    def __init__(self , spriteshape , color , startx , starty):
        sprite.__init__(self , spriteshape , color , startx , starty)
        self.speed = 6
        self.setheading(random.randint(0 , 360))#so that it moves in all direction not just one
#______________________________________________________________________________________________________________________
#ally
class ally(sprite):
    def __init__(self,spriteshape,color,startx,starty):
        sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed = 8
        self.setheading(random.randint(0 , 360))
# method for movement
    def move(self):
        self.fd(self.speed)
#boundary detection(cannot cross the boundary):
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)


        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)
#______________________________________________________________________________________________________________________
# missile
class missile(sprite):
    def __init__(self , spriteshape , color , startx , starty):
        sprite.__init__(self , spriteshape , color , startx , starty)
        self.shapesize(stretch_wid=0.2,stretch_len=0.4,outline=None)#to make it smaller than others
        self.speed = 20
        self.status = "ready"#so that missile is ready to use but not shown at first
        self.goto(-1000,1000)
#______________________________________________________________________________________________________________________
#fire method
    def fire(self):
# sound after missile is fired:
        winsound.PlaySound("machine-gun-01.wav", winsound.SND_ASYNC)
        if self.status=="ready":
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status="firing"
# overriding the prev move method(movement for shoot)
    def move(self):
        if self.status == "ready":
            self.goto(-1000,1000)
        if self.status =="firing":
            self.fd(self.speed)
#  border check
        if self.xcor() < -290 or self.xcor() > 290 or \
                self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000,1000)
            self.status = "ready"# explosion:
class particle(sprite):
    def __init__(self , spriteshape , color , startx , starty):
        sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, 1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1
        if self.frame > 15:
            self.frame = 0
            self.goto(-1000, 1000)
# ................................................................................................................................
# description about the game
class game():
    def __init__(self):
        self.level=1
        self.score=0
        self.state = "playing"
        self.pen=turtle.Turtle()
        self.lives =3

# border for the game:
    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(7)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
            self.pen.penup()
            self.pen.ht()
            self.pen.pendown()

#______________________________________________________________________________________________________________________
# method for score:to display score
    def show_status(self):# score is overlapping on each othher , so solving that problem
         self.pen.undo()
         mssg = "SCORE : %s" %(self.score)
         self.pen.penup()
         self.pen.goto(-300,310)
         self.pen.write(mssg,font=("Arial",13,"bold"))

# create game object
Game = game()# draw the game border
Game.draw_border()# show the score
Game.show_status()

# .................................................................................................................................
# creating the 'sprites'(objects on the screens(player,missile,enemy,ally):
player = player( 'triangle','brown',0,0)
#enemy = enemy('circle','orange',-100,0)
missile = missile('triangle','blue',0,0)
#ally = ally('square','blue',0,0)
enemies=[]
for a in range(10):#for loop so multiple enemies shows
    enemies.append(enemy('circle','pink',-100,0))
allys=[]
for a in range(9):#for loop so multiple allys shows
    allys.append(ally('square','orange',0,0))
particles =[]
for a in range(20):
    particles.append(particle('circle','orange',0,0))

#___________________________
# key bindings:
#left
turtle.onkey(player.turn_left,"Left")
# right
turtle.onkey(player.turn_right,"Right")
# accelerate
turtle.onkey(player.accelerate,"Up")
# decelerate
turtle.onkey(player.deaccelerate,"Down")
# firing
turtle.onkey(missile.fire,"space")
turtle.listen()


# .............................................................................................................................
# (MOVEMENT OF OBJECTS ON SCREEN)-now we got to move the objects on the screen so we apply while loop:
while True:
    turtle.update()#update the screen so the movement happens properly and in good speed
    time.sleep(0.02)
    player.move()
    missile.move()
# ally.move()
    for enemy in enemies:
        enemy.move()
 # check for collision between player and enemy
        if player.is_collision(enemy):
 # sound after missile is fired:
            winsound.PlaySound("breaking-glass-82857.wav", winsound.SND_ASYNC)
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            Game.score -= 100
            Game.show_status()
# check for collision between missile and enemy:
        if missile.is_collision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            missile.status = "ready"
# if collision between missile and enemy , then score will be increased
            Game.score +=100
            Game.show_status()
# explosion occurs here:
            for particle in particles:
                particle.explode(missile.xcor(),missile.ycor())
            for ally in allys:
                ally.move()
# check for collision between missile and ally
                if missile.is_collision(ally):
                    x = random.randint(-250,250)
                    y = random.randint(-250,250)
                    ally.goto(x,y)
                    missile.status ="ready"
# if collision between missile and ally , then score will be decreased
                    Game.score -=50
                    Game.show_status()
            for particle in particles:
                particle.move()

