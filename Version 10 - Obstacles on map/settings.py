import pygame, os
from pygame.math import Vector2

# All time-related things are in milliseconds eg. "BULLET_LIFETIME"

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0 ,0)
YELLOW = (255, 255, 0)
BLUE = (0 ,0 ,255)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# Game settings
TITLE = "My Game"
WIDTH = 1024 # 16 * 64 OR 32 * 32 OR 64 * 16
HEIGHT = 768 # 16 * 48 OR 32 * 24 OR  64 * 12
FPS = 60
BGCOLOUR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
map_folder = os.path.join(game_folder, "maps")
# Images
WALL_IMG = "tileGreen_39.png"
PLAYER_IMG = "manBlue_gun.png"
BULLET_IMG = "bullet.png"

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 250
PLAYER_HIT_BOX = pygame.Rect(0, 0, 35, 35)
BARREL_OFFSET = Vector2(30, 10)
# Gun settings
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
FIRE_RATE = 150
KICK_BACK = 200
BULLET_SPREAD = 5
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = "zoimbie1_hold.png"
MOB_SPEED = 150
MOB_HIT_BOX = pygame.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_ATTACK_SPEED = 500
MOB_KNOCKBACK = 10