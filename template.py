import pygame, sys, random, os
from pygame.locals import *
from settings import *
from sprites import *

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    #update
    all_sprites.update()
    
    #draw        
    screen.fill(RED)
    all_sprites.draw(screen)
    
    #update diplay
    pygame.display.update()
    #print(clock.get_fps())
    clock.tick(FPS)