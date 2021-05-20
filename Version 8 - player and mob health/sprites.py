import pygame
from pygame.locals import *
from pygame.math import Vector2
from tilemap import collide_hit_box
from settings import *
from sprites import *
from random import uniform

def collide_with_walls(sprite, group, dir):
        if dir == "x":
            hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
            if hits:
                if hits[0].rect.centerx > sprite.hit_box.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_box.width / 2
                if hits[0].rect.centerx < sprite.hit_box.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_box.width / 2
                sprite.vel.x = 0
                sprite.hit_box.centerx = sprite.pos.x
        if dir == "y":
            hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
            if hits:
                if hits[0].rect.centery > sprite.hit_box.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_box.height / 2
                if hits[0].rect.centery < sprite.hit_box.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_box.width / 2
                sprite.vel.y = 0
                sprite.hit_box.centery = sprite.pos.y

class Player(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_box = PLAYER_HIT_BOX
        self.hit_box.center = self.rect.center
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
            
    def get_keys(self):
        self.rot_speed = 0
        self.vel = Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[K_d] or keys[K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[K_w] or keys[K_UP]:
            self.vel = Vector2(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[K_s] or keys[K_DOWN]:
            self.vel = Vector2(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > FIRE_RATE:
                self.last_shot = now
                dir = Vector2(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel = Vector2(-KICK_BACK, 0).rotate(-self.rot)
    
    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_box.center
        
class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_box = MOB_HIT_BOX.copy()
        self.hit_box.center = self.rect.center
        self.pos = Vector2(x, y) * TILESIZE
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0) # Acceleration
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.last_hit = 0
        
    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to((Vector2(1, 0)))
        self.image = pygame.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = Vector2(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_box.center
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health / MOB_HEALTH * 100 > 60:
            col = GREEN
        elif self.health / MOB_HEALTH * 100 > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.rect.center = pos
        spread = uniform(-BULLET_SPREAD, BULLET_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED * self.game.dt
        self.spawn_time = pygame.time.get_ticks()
        
    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE