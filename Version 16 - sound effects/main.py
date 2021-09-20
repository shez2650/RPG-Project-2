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
        pygame.mixer.pre_init(22050, -16, 1, 2048)
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(300, 75)
        self.running = True
        self.draw_debug = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.load_data()
    
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        try:
            font = pygame.font.Font(font_name, size)
        except:
            font = pygame.font.SysFont(font_name, size)
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "centre":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def load_data(self):
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pygame.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pygame.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pygame.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pygame.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gun_flashes = [pygame.image.load(dir).convert_alpha() for dir in MUZZLE_FLASHES]
        self.item_images = {k:pygame.image.load(path.join(img_folder, i)) for (k,i) in ITEM_IMAGES.items()}
        
        # Sounds
        pygame.mixer.music.load(os.path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {k:pygame.mixer.Sound(path.join(sfx_folder, v)) for (k,v) in EFFECTS_SOUNDS.items()}
        
    
    def new(self):
        # start a new game
        self.effects_sounds["level_start"].play()
        pygame.mixer.music.play(-1)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.map = TileMap(path.join(map_folder, "game_map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.timer = 0
        
        # load map
        for tile_object in self.map.tmxdata.objects:
            obj_center = Vector2(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height /2)
            if tile_object.name == "Player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "Mob":
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == "Wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ["health"]:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        
    
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
        self.timer = pygame.time.get_ticks() - self.start_time
        
        # Game Loop - update
        self.all_sprites.update()
        self.camera.update(self.player)
        
        #game over?
        if not len(self.mobs):
            self.playing = False
        
        # player hits items
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                if self.player.health + HEALTH_PACK_AMOUNT > PLAYER_HEALTH:
                    self.player.health == PLAYER_HEALTH
                else:
                    self.player.health += HEALTH_PACK_AMOUNT
        
        # mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_box)
        for hit in hits:
            now = pygame.time.get_ticks()
            if now - hit.last_hit > MOB_ATTACK_SPEED:
                hit.last_hit = now
                self.player.health -= MOB_DAMAGE
                hit.vel = Vector2(0, 0)
            if self.player.health <= 0:
                self.player.dead = True
                self.playing = False
        if hits:
            self.player.pos += Vector2(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        
        # bullets hit mobs
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.hit = True
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
            if self.draw_debug and not isinstance(sprite, MuzzleFlash):
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_box), 1)
                
        # debug
        if self.draw_debug:
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
        self.draw_text(f"Zombies: {len(self.mobs)}", HUD_FONT, 30, WHITE, WIDTH-10, 10, align="ne")
        pygame.display.flip()
    
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.player.dead = True
                    self.playing = False
                if event.key == K_h:
                    self.draw_debug = not self.draw_debug
    
    def show_start_screen(self):
        # Game start screen
        pass
    
    def show_game_over_screen(self):
        pygame.mixer.music.fadeout(1000)
        # Saving timer
        millis = self.timer%1000
        seconds = int(self.timer/1000 % 60)
        minutes = int(self.timer/60000 % 24)
        total_millis = self.timer
        score = f"{minutes}m {seconds}s {millis}ms"
        # Check if the highscore has been beaten
        try:
            with open("highscore.txt", "r") as file:
                data = [int(line.strip("\n")) for line in file.readlines()]
                highscore = f"{data[2]}m {data[1]}s {data[0]}ms"
                hsmillis = data[2]*60000 + data[1]*1000 + data[0]
            
            if not self.player.dead and total_millis < hsmillis:
                highscore = f"{minutes}m {seconds}s {millis}ms"
                with open("highscore.txt", "w") as file:
                    file.write(f"{millis}\n")
                    file.write(f"{seconds}\n")
                    file.write(str(minutes))
        except FileNotFoundError:
            if self.player.dead:
                highscore = "N/A"
            else:
                highscore = f"{minutes}m {seconds}s {millis}ms"
                with open("highscore.txt", "w") as file:
                    file.write(f"{millis}\n")
                    file.write(f"{seconds}\n")
                    file.write(str(minutes))
                
        # Game over/continue screen
        self.screen.fill(BLACK)
        if self.player.dead:
            self.draw_text("GAME OVER", TITLE_FONT, 100, RED, WIDTH / 2, HEIGHT / 2, align="centre")
        else:
            self.draw_text("YOU WIN!", TITLE_FONT, 100, GREEN, WIDTH / 2, HEIGHT / 2, align="centre")
        self.draw_text("Press space bar to start", TITLE_FONT, 75, WHITE, WIDTH/2, HEIGHT * 3/4, align="centre")
        self.draw_text(f"Current Score:  {score}         Highscore:  {highscore}", None, 24, CYAN, WIDTH/2, HEIGHT * 1/4, align="centre")
        pygame.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        self.pressed = False
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.quit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.pressed = True
                if self.pressed and event.type == KEYUP and event.key == K_SPACE:
                    waiting = False
    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_game_over_screen()
    
pygame.quit()