import os
import sys
import math
import random

import json
import pygame
import time

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy, Boss
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.pyvidplayer import Video


LEVEL_TEXTS = ["Anastasia's Heavens", "Baldan's Mountains", "Timur's City", "Sofie's Cave", "Joubran's Hell", "THE DOROCK DUNGEON"]


class Game:
    def __init__(self, menu, svol, vol):
        pygame.init()
        pygame.display.set_caption('DOROCK')

        self.menu = menu

        self.WINDOW_WIDTH = 320
        self.WINDOW_HEIGHT = 240
        self.screen = pygame.display.set_mode((1280,720))
        self.display = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'cave_dirt': load_images('tiles/cave_dirt'),
            'cave_stone': load_images('tiles/cave_stone'),
            'city_brick': load_images('tiles/city_brick'),
            'city_rock': load_images('tiles/city_rock'),
            'heaven_grass': load_images('tiles/heaven_grass'),
            'heaven_stone': load_images('tiles/heaven_stone'),
            'hell_lava_blocks': load_images('tiles/hell_lava_blocks'),
            'hell_bricks': load_images('tiles/hell_bricks'),
            'hell_grass': load_images('tiles/hell_grass'),
            'hell_stone': load_images('tiles/hell_stone'),
            'portal_block': load_images('tiles/portal_block'),
            'barrier' : load_images('tiles/barrier'),

            'player': load_image('entities/player.png'),

            'background0': load_image('background0.png'),
            'background1': load_image('background1.png'),
            'background2': load_image('background2.png'),
            'background3': load_image('background3.png'),
            'background4': load_image('background4.png'),
            'background5': load_image('background5.png'),

            'clouds': load_images('clouds'),
            'hell_clouds': load_images('hell_clouds'),
            'no_clouds': load_images('no_clouds'),

            'health': load_images('health'),
            'lava' : load_images('tiles/lava'),

            'e0/idle': Animation(load_images('entities/e0/idle'), img_dur=6),
            'e0/run': Animation(load_images('entities/e0/run'), img_dur=4),
            'e1/idle': Animation(load_images('entities/e1/idle'), img_dur=6),
            'e1/run': Animation(load_images('entities/e1/run'), img_dur=4),
            'e2/idle': Animation(load_images('entities/e2/idle'), img_dur=6),
            'e2/run': Animation(load_images('entities/e2/run'), img_dur=4),
            'e3/idle': Animation(load_images('entities/e3/idle'), img_dur=6),
            'e3/run': Animation(load_images('entities/e3/run'), img_dur=4),
            'e4/idle': Animation(load_images('entities/e4/idle'), img_dur=6),
            'e4/run': Animation(load_images('entities/e4/run'), img_dur=4),

            'boss/idle': Animation(load_images('entities/boss/idle'), img_dur=8),
            'boss/attack_rocks': Animation(load_images('entities/boss/attack_rocks'), img_dur=8),
            'boss/attack_chains': Animation(load_images('entities/boss/attack_chains'), img_dur=8),
            'boss/attack_chains_2': Animation(load_images('entities/boss/attack_chains_2'), img_dur=8),
            'boss/weakened': Animation(load_images('entities/boss/weakened'), img_dur=8),

            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),

            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'projectile': load_image('projectile.png'),
            'chain': load_image('chain.png'),
            'lava_ball': load_image('lava_ball.png'),
        }
        
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'explosion': pygame.mixer.Sound('data/sfx/explosion.wav')
        }   

        self.volume = vol

        self.sfx['ambience'].set_volume(0*svol)
        self.sfx['shoot'].set_volume(0.1*svol)
        self.sfx['hit'].set_volume(0.2*svol)
        self.sfx['dash'].set_volume(0.2*svol)
        self.sfx['jump'].set_volume(0.2*svol)
        self.sfx['explosion'].set_volume(0.2*svol)

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))
        self.last_dmg_call = 0

        self.tilemap = Tilemap(self, tile_size=16)
        self.ground_offset = 2

        self.level = 0

        if self.level == 5:
            self.boss = Boss(self, (0,0), (96,96))

        self.max_enemies = 1
        
        try:
           self.load_level_save('level.json')
        except FileNotFoundError:
           pass

        self.current_music = -1
        self.screenshake = 0
        self.next_level = False

        self.load_level(self.level)

        self.font = pygame.font.SysFont(None, 25)
        
        self.last_txt_call = 0
        self.running = False

    def load_level(self, map_id):
        if self.current_music != self.level:
            pygame.mixer.music.load('data/music/' + str(self.level) + '.mp3')
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.current_music = self.level

        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2), ('decor', 7)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
            
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                if(map_id != 5):
                    self.enemies.append(Enemy(self, spawner['pos'], (16, 25), 'e' + str(map_id)))
                else:
                    self.boss = Boss(self, spawner['pos'], (96,96))
                    self.enemies.append(self.boss)

        for door in self.tilemap.extract([('decor', 4)], True):
            self.door_rec = pygame.Rect(door['pos'][0], door['pos'][1], 48, 16)
        
        if map_id == 5:
            self.ground_offset = 1.3
        else:
            self.ground_offset = 2

        if map_id == 3:
            self.clouds = Clouds(self.assets['no_clouds'], count=16)
        elif map_id > 3:
            self.clouds = Clouds(self.assets['hell_clouds'], count=16)

        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -80
        self.next_level = False
        self.last_txt_call = 0
        self.player.health = self.player.max_health
        self.max_enemies = len(self.enemies)
        
    def run(self):        
        self.sfx['ambience'].play(-1)
        
        if self.level == 0:
            self.PlayVid('data/cutscenes/intro.mp4')
        else:
            self.running = True

        while True:
            if not self.running:
                continue

            if not pygame.mixer.music.get_busy():
                pass
                pygame.mixer.music.play()

            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets['background' + str(self.level)], (0, 0))
            
            self.screenshake = max(0, self.screenshake - 1)

            if len(self.enemies) <= (self.max_enemies / 4) * 3:
                self.sfx['explosion'].play()
                self.max_enemies = -1
                for portal in self.tilemap.extract([('portal_block', 0)]):
                    pass

            if self.level < 5:
                if self.player.rect().colliderect(self.door_rec):
                    self.next_level = True

            if self.next_level:
                self.save_level('level.json')
                self.transition += 1
                if self.transition > 80:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)

            if self.transition < 0:
                self.transition += 1
            
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / self.ground_offset - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
            # [[x, y], directionx, directiony, timer, img]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[0][1] += projectile[2]
                projectile[3] += 1

                self.display.blit(projectile[4], (projectile[0][0] - projectile[4].get_width() / 2 - render_scroll[0], projectile[0][1] - projectile[4].get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[3] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.take_damage(1)
                        
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
                    
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            self.display.blit(self.assets['health'][self.player.health - 1], (8,8))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                    if event.key == pygame.K_n:
                        self.next_level = True
                    if event.key == pygame.K_f:
                        width, height = self.screen.get_size()
                        if width == 1280:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((1280,720))
                    if event.key == pygame.K_r:
                        self.load_level(self.level)
                    if event.key == pygame.K_n:
                        self.next_level = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
            
            if self.last_txt_call < 240:
                #outline
                self.show_text(LEVEL_TEXTS[self.level],[2,-2], (1,1,1))
                self.show_text(LEVEL_TEXTS[self.level],[-2,2], (1,1,1))
                self.show_text(LEVEL_TEXTS[self.level],[-2,-2], (1,1,1))
                self.show_text(LEVEL_TEXTS[self.level],[2,2], (1,1,1))
                #text
                self.show_text(LEVEL_TEXTS[self.level],[0,0])

                self.last_txt_call += 1

            self.display_2.blit(self.display, (0, 0))
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)

            pygame.display.update()
            self.clock.tick(60)

    def show_text(self,text, offset = [0,0], color = (255,255,255)):
        text = self.font.render(text,True,color)
        text_rect = text.get_rect()
        text_rect.center = (self.WINDOW_WIDTH // 2 + offset[0], self.WINDOW_HEIGHT // 4 + offset[1])
        self.display.blit(text, text_rect)

    def take_damage(self, damage):
        if time.time() - self.last_dmg_call < 2:
            return 

        self.player.health -= damage

        self.sfx['hit'].play()
        self.screenshake = max(16, self.screenshake)
        for i in range(30):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5
            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
        if self.player.health <= 0: 
            if self.dead > 0:
                return
            self.dead += 1
            self.player.health = self.player.max_health
        self.last_dmg_call = time.time()

    def PlayVid(self, vid_name, quit=False):
        self.display = pygame.Surface((1280, 960), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((1280, 960))

        pygame.mixer.music.stop()
        vid = Video(vid_name)
        self.running = False
        while True:
            vid.draw(self.display, (0, 0), force_draw=False)
            self.display_2.blit(self.display, (0, 0))
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0,0))

            pygame.display.update()
            self.clock.tick(60)

            if not vid.active:
                vid.close()
                self.display = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
                self.display_2 = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                self.running = True
                if quit:
                    pygame.quit()
                    sys.exit()
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        width, height = self.screen.get_size()
                        if width == 1280:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((1280,720))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    vid.close()
                    self.display = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
                    self.display_2 = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                    self.running = True
                    return

    def save_level(self, path):
        f = open(path, 'w')
        json.dump(self.level + 1, f)
        f.close()

    def load_level_save(self, path):
        f = open(path, 'r')
        self.level = json.load(f)
        f.close()
