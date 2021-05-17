import pygame, sys, random
from os import path
from pygame.locals import *
from settings import *
from sprites import *

class Game():
    def __init__(self):
        # Initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(300, 75)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
    
    def load_data(self):
        self.map_data = []
        with open(path.join(game_folder, "map.txt"), "r") as f:
            for line in f:
                self.map_data.append(line)
    
    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.load_data()
        self.walls = pygame.sprite.Group()
        for y, tiles in enumerate(self.map_data):
            for x, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, x, y)
                if tile == "P":
                    self.player = Player(self, x, y)
                    
        g.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def update(self):
        # Game Loop - update
        self.all_sprites.update()
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOUR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
    
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                
                if event.key == K_a:
                    self.player.move(dx = -1)
                elif event.key == K_d:
                    self.player.move(dx = 1)
                elif event.key == K_s:
                    self.player.move(dy = 1)
                elif event.key == K_w:
                    self.player.move(dy = -1)
    
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