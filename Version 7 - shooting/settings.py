import pygame, os

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

# Player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_HIT_BOX = pygame.Rect(0, 0, 35, 35)

# Mob settings
MOB_IMG = "zoimbie1_hold.png"
MOB_SPEED = 150
MOB_HIT_BOX = pygame.Rect(0, 0, 30, 30) 