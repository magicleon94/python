import sys
import pygame
pygame.init()

class Player:
    def __init__(self,image,height,speed):
        self.image = image
        self.speed = speed
        self.pos = image.get_rect().move(0,height)
    def move(self):
        self.pos = self.pos.move(self.speed,0)
        if self.pos.right >600:
            self.pos.left = 0
    def move_down(self):
        self.pos = self.pos.move(0,self.speed)
    def move_up(self):
        self.pos = self.pos.move(0,-self.speed)
    def move_right(self):
        self.pos = self.pos.move(self.speed,0)
    def move_left(self):
        self.pos = self.pos.move(-self.speed,0)

black = 0,0,0

screen = pygame.display.set_mode((600,200))
player1_img = pygame.image.load("1.gif")
player2_img = pygame.image.load("2.gif")
player3_img = pygame.image.load("3.gif")

objects = []
x = Player(player1_img,10,5)
objects.append(x)
x =Player(player2_img,40,10)
objects.append(x)

player = Player(player3_img,70,10)

w = pygame.K_UP
a = pygame.K_LEFT
s = pygame.K_DOWN
d = pygame.K_RIGHT
#print ("Setup completed")
while 1:
    screen.fill(black)
    for event in pygame.event.get():
 #       print (event)
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == s: #pygame.K_DOWN:
                player.move_down()
            if event.key == w: #pygame.K_UP:
                player.move_up()
            if event.key == a: #pygame.K_LEFT:
               player.move_left()
            if event.key == d: #pygame.K_RIGHT:
                player.move_right()
    for o in objects:
        o.move()
        screen.blit(o.image,o.pos)
	screen.blit(player.image,player.pos)  
    pygame.display.update()
    pygame.time.delay(20)
        
