import pygame, math
from pygame.locals import *
from pygame.math import Vector2
from tilemap import collide_hit_box
from settings import *
from random import randint, uniform, choice

def sine_based_animation(n):
    return -0.5 * (math.cos(math.pi * n) - 1)

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
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_box = PLAYER_HIT_BOX
        self.hit_box.center = self.rect.center
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y)
        self.rot = -90
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
                if not any(isinstance(sprite, MuzzleFlash) for sprite in self.game.all_sprites):
                    MuzzleFlash(self.game, pos)
    
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
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_box = MOB_HIT_BOX.copy()
        self.hit_box.center = self.rect.center
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0) # Acceleration
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.last_hit = 0
        self.speed = choice(MOB_SPEEDS)
        self.hit = False
        self.chasing_player = False
        self.chasing_mob = False
        self.found = False
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()
        
    def update(self):
        dist = (self.game.player.pos - self.pos).length()

        if self.hit == True:
            if CHASE_RADIUS * 1.5 > dist > CHASE_RADIUS:
                self.chasing_player = True
            else:
                self.hit = False
                self.chasing_player = False
                self.vel = Vector2(0, 0)
                self.acc = Vector2(0, 0)
            
        if self.chasing_player == False and self.hit == False:
            for mob in self.game.mobs:
                if mob != self and (mob.pos - self.pos).length() < AWARENESS_RADIUS and mob.chasing_player == True:
                    self.found = True
                    break
                else:
                    self.found = False
            
            if self.found:
                self.chasing_mob = True
            else:
                self.chasing_mob = False
                if not self.chasing_player:
                    self.vel = Vector2(0, 0)
                    self.acc = Vector2(0, 0)
        
        if dist < CHASE_RADIUS:
            self.chasing_player = True
                    
        if not (self.chasing_player == False) and not (self.hit == True) and not (dist < CHASE_RADIUS) and not (self.chasing_player == False and self.hit == False):
            self.chasing_player = False
            self.chasing_mob = False
            self.vel = Vector2(0, 0)
            self.acc = Vector2(0, 0)
            
        if self.chasing_player:
            self.move(self.game.player)
        elif self.chasing_mob:
            self.move(mob)
        
        self.image = pygame.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_box.center
        if self.health <= 0:
            if self.game.player.health + 20 > PLAYER_HEALTH:
                self.game.player.health = PLAYER_HEALTH
            else:
                self.game.player.health += 20
            self.kill()
    
    def move(self, target):
        self.rot = (target.pos - self.pos).angle_to((Vector2(1, 0)))
        self.acc = Vector2(1, 0).rotate(-self.rot)
        if target == self.game.player:
            self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
    
    def draw_health(self):
        if self.health / MOB_HEALTH * 100 > 60:
            col = GREEN
        elif self.health / MOB_HEALTH * 100 > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.hit_box.width * self.health / MOB_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_box = self.rect
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
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_box = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(*FLASH_SIZES)
        self.image = pygame.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pygame.time.get_ticks()
        #print([sprite for sprite in self.game.all_sprites if isinstance(sprite, MuzzleFlash)])
        
    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()