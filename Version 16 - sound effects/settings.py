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
#----------------------------------------------------
# Game settings
TITLE = "My Game"
FPS = 60
WIDTH = 1024 # 16 * 64 OR 32 * 32 OR 64 * 16
HEIGHT = 768 # 16 * 48 OR 32 * 24 OR  64 * 12
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
BGCOLOUR = BROWN
#----------------------------------------------------
# Assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
music_folder = os.path.join(game_folder, "music")
map_folder = os.path.join(game_folder, "maps")
# Images
WALL_IMG = "tileGreen_39.png"
PLAYER_IMG = "manBlue_gun.png"
MOB_IMG = "zoimbie1_hold.png"
BULLET_IMG = "bullet.png"
TITLE_FONT = os.path.join(img_folder, "ZOMBIE.TTF")
HUD_FONT = os.path.join(img_folder, "Impacted2.0.ttf")
MUZZLE_FLASHES = [os.path.join(game_folder, img) for img in os.scandir("img\White puff")]
ITEM_IMAGES = {"health":"health_pack.png"}
#----------------------------------------------------
# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 250
PLAYER_HIT_BOX = pygame.Rect(0, 0, 35, 35)
BARREL_OFFSET = Vector2(30, 10)
# Gun settings
BULLET_SPEED = 500
BULLET_LIFETIME = 750
FIRE_RATE = 150
KICK_BACK = 200
BULLET_SPREAD = 5
BULLET_DAMAGE = 10
# Vfx
FLASH_DURATION = 40
FLASH_SIZES = (20, 60)
#----------------------------------------------------
# Mob settings
MOB_SPEEDS = [125, 150, 175, 200]
MOB_HIT_BOX = pygame.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_ATTACK_SPEED = 500
MOB_KNOCKBACK = 10
CHASE_RADIUS = 300
AWARENESS_RADIUS = 250
AVOID_RADIUS = 50
#----------------------------------------------------
#Layers
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4
#----------------------------------------------------
#Items
HEALTH_PACK_AMOUNT = 20