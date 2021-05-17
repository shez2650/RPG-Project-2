import pygame, sys, random, os
from pygame.locals import *
from settings import *
from sprites import *

class Player(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[K_d] or keys[K_RIGHT]:
            self.vx = PLAYER_SPEED
        if keys[K_w] or keys[K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[K_s] or keys[K_DOWN]:
            self.vy = PLAYER_SPEED
            
        # Diaganol since movement in both axis
        if self.vx != 0 and self.vy != 0:
            # Divide by sqr of 2 so diagonal is not faster (Pythagoras Theorem)
            self.vx /= 1.414
            self.vy /= 1.414
        
    
    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == "y":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls("x")
        self.rect.y = self.y
        self.collide_with_walls("y")
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE