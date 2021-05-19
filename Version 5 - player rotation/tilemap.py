import pygame, sys, random
from os import path
from pygame.locals import *
from settings import *
from sprites import *

def collide_hit_box(one, two):
    return one.hit_box.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(path.join(filename), "r") as f:
            for line in f:
                self.data.append(line)
                
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.centerx + WIDTH // 2
        y = -target.rect.centery + HEIGHT // 2
        
        # Limit scrolling to map size
        x = min(0, x) # left
        x = max(-(self.width - WIDTH - TILESIZE), x) # right
        y = min(0, y) # top
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)