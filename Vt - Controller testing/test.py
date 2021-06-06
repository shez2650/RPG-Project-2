import pygame, sys, os
from pygame.locals import *
pygame.init()
pygame.display.set_caption("controller testing")
screen = pygame.display.set_mode((500, 500), 0 , 32)
clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)

my_square = pygame.Rect(50, 50, 50, 50)
my_square_colour = 0
colours = [(255, 0 , 0), (0, 255, 0), (0, 0, 255)]
motion = [0, 0]

while True:
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, colours[my_square_colour], my_square)
    my_square.x += motion[0] * 10
    my_square.y += motion[1] * 10
    
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            print(event)
        if event.type == JOYBUTTONUP:
            print(event)
        if event.type == JOYAXISMOTION:
            print(event)
        if event.type == JOYHATMOTION:
            print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    pygame.display.update()
    clock.tick(60)