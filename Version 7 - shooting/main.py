import pygame, sys, random
from os import path
from pygame.locals import *
from settings import *
from sprites import *
from tilemap import *

class Game():
    def __init__(self):
        # Initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(300, 75)
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()
    
    def load_data(self):
        self.map = Map(path.join(map_folder, "map3.txt"))
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pygame.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pygame.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pygame.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pygame.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
    
    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # load the map
        for y, tiles in enumerate(self.map.data):
            for x, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, x, y)
                if tile == "P":
                    self.player = Player(self, x, y)
                if tile == "M":
                    Mob(self, x, y)
        
        self.camera = Camera(self.map.width, self.map.height)
        
        g.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def update(self):
        # Game Loop - update
        self.all_sprites.update()
        self.camera.update(self.player)
        # bullets hit mobs
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.kill()
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        # Game Loop - draw
        
        # Set caption to FPS
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOUR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #pygame.draw.rect(self.screen, WHITE, self.player.hit_box, 2)
        pygame.display.flip()
    
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
    
    def show_start_screen(self):
        # Game start screen
        pass
    
    def show_go_screen(self):
        # Game over/continue screen
        pass
    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    
pygame.quit()