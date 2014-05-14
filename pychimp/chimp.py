import sys
import os
import pygame
#from pygame.local import *

def load_image(name, colorkey = None):
   # fullname = os.path.join('data',name)
    try:
        image = pygame.image.load(name)#fullname)
    except pygame.error, message:
        print 'Cannot load image:' + str(name)
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)#,RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data',name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:' + str(wav)
        raise SystemExit, message
    return sound

class Fist(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('2.gif',-1)
        self.punching = 0
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5,10)
    def punch(self,target):
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5,-5)
            return hitbox.colliderect(target.rect)
    def unpunch(self):
        self.punching = 0

class Chimp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('3.gif',-1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10,60
        self.move = 9
        self.dizzy = 0
    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._walk()
    def _walk(self):
        newpos = self.rect.move((self.move,0))
        #if not self.area.contains(newpos): 
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move,0))
                self.image = pygame.transform.flip(self.image,1,0)
        self.rect = newpos
    def _spin(self):
        center = self.rect.center
        self.dizzy+=10
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original,self.dizzy)
        self.rect = self.image.get_rect(center = center)
    def punched(self):
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
#####################    MAIN    #####################
pygame.init()
screen = pygame.display.set_mode((500,200))
pygame.display.set_caption('Monkey Fever')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,250,250))

if pygame.font:
    font = pygame.font.Font(None,36)
    text = font.render("Hit the Chimp, and win $$$",1,(10,10,10))
    textpos = text.get_rect(centerx = background.get_width()/2)
    background.blit(text,textpos)
screen.blit(background,(0,0))
pygame.display.flip()

whiff_sound = load_sound('whiff.wav')
punch_sound = load_sound('punch.wav')
chimp = Chimp()
fist = Fist()
allsprites = pygame.sprite.RenderPlain((fist,chimp))
clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()# return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()#return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fist.punch(chimp):
                punch_sound.play()
                chimp.punched()
            else:
                whiff_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            fist.unpunch()
    allsprites.update()
    screen.blit(background,(0,0))
    allsprites.draw(screen)
    pygame.display.flip()


