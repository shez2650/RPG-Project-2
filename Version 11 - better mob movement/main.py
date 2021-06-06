import pygame, sys
from os import path
from pygame.locals import *
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_WIDTH = 150
    BAR_HEIGHT = 30
    fill = percent * BAR_WIDTH
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if percent > 0.6:
        col = GREEN
    elif percent > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Game():
    def __init__(self):
        # Initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(300, 75)
        self.running = True
        self.draw_debug = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()
    
    def load_data(self):
        self.map = TileMap(path.join(map_folder, "game_map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
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
        
        # load map
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "Player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "Mob":
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == "Wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
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
        # mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_box)
        for hit in hits:
            now = pygame.time.get_ticks()
            if now - hit.last_hit > MOB_ATTACK_SPEED:
                hit.last_hit = now
                self.player.health -= MOB_DAMAGE
                hit.vel = Vector2(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += Vector2(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        
        # bullets hit mobs
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = Vector2(0, 0)
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        # Game Loop - draw
        
        # Set caption to FPS
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOUR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply_sprite(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_box), 1)

        # debug
        if self.draw_debug:
            # draw_hitboxes
            for wall in self.walls:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.hit_box), 1)
            
            # draw coordinates
            font = pygame.font.SysFont(None, 16)
            x = font.render(f"x: {round(self.player.pos.x, 2)}", True, BLACK)
            y = font.render(f"y: {round(self.player.pos.y, 2)}", True, BLACK)
            
            pygame.Surface.blit(self.screen, x, (10, 35 + x.get_height()))
            pygame.Surface.blit(self.screen, y, (10, 40 + x.get_height() + y.get_height()))
            
        #pygame.draw.rect(self.screen, WHITE, self.player.hit_box, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pygame.display.flip()
    
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.playing = False
                if event.key == K_h:
                    self.draw_debug = not self.draw_debug
    
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