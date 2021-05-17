import pygame, sys, random, os
from pygame.locals import *
from pygame.math import Vector2
from settings import *
from sprites import *


class Player(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y) * TILESIZE
            
    def get_keys(self):
        self.vel = Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[K_d] or keys[K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if keys[K_w] or keys[K_UP]:
            self.vel.y = -PLAYER_SPEED
        if keys[K_s] or keys[K_DOWN]:
            self.vel.y = PLAYER_SPEED
        
        # Diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            # Divide by sqr of 2 so diagonal is not faster (Pythagoras Theorem)
            self.vel /= 1.414
        
    
    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    
    
    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE