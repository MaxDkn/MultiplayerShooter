import sys
import pickle
import pygame
from walls import Walls
from player import Player
from network import Network
from bullet import draw_bullet
from time_management import TimeManagement
from information_panel import LevelInformationDraw
from config import MAP, TILE_SIZE, damage, velocity_bullet
from utils import get_wall_name, calcul_vector, get_actually_bullet_pos


class Level:
    def __init__(self, setting):
        self.setting = setting

        self.screen = pygame.display.get_surface()
        pygame.display.set_caption(f'Shooter Game')

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.clock = pygame.time.Clock()

        self.network = Network(self.setting.address, setting.port)

        self.walls = []

        self.player_count = int(self.network.get_player_count())
        self.game_state = self.network.send('get')

        if self.player_count == 0:
            self.other_player_count = 1
        else:
            self.other_player_count = 0

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.other_player = Player(
            self.game_state[self.other_player_count]['pos'], self.all_sprites, self.collision_sprites)
        self.player = Player(self.game_state[self.player_count]['pos'], self.all_sprites, self.collision_sprites)

        self.import_walls()
        self.all_sprites.add(self.walls)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.other_player)
        self.collision_sprites.add(self.other_player)

        self.text_management = LevelInformationDraw(self.screen, self.player, self.network)
        self.time_management = TimeManagement()
        self.bullets = []

    def import_walls(self):
        for height_count, height_element in enumerate(MAP):
            for width_count, width_element in enumerate(height_element):
                if width_element == 1:
                    wall = Walls((width_count * TILE_SIZE[0], height_count * TILE_SIZE[1] + 50),
                                 get_wall_name(width_count, height_count), [self.all_sprites, self.collision_sprites])

                    self.collision_sprites.add(wall)
                    self.walls.append(wall)

    def run(self):
        run = True
        while run:
            mouse_clicked = False
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True

            if not self.game_state['ready']:
                to_send = 'get'
                self.waiting_room()

            else:
                to_send = {
                    'pos': (int(self.player.pos.x), int(self.player.pos.y)),
                    'angle': int(self.player.angle),
                    'current_gun': self.player.current_gun,
                    'bullets': self.bullets,
                    'heal_point': self.player.heal,
                }

                to_send = pickle.dumps(to_send)
                self.main_room(dt, mouse_clicked)

                self.time_management.update_time(pygame.time.get_ticks())
                self.time_management.get_game_time()

            try:
                self.game_state = self.network.send(to_send)
            except EOFError:
                run = False
            pygame.display.update()

    def main_room(self, dt, mouse_clicked):
        self.clear_border_sprite()

        self.player.input()
        if mouse_clicked and self.player.current_gun != 'run' and self.player.alive:
            direction = calcul_vector(self.player.pos, pygame.mouse.get_pos())

            bullet_will_not_touch_a_wall = True
            for wall in self.walls:
                if wall.hit_box.collidepoint((self.player.rect.centerx + direction.x * 25, self.player.rect.centery +
                                              direction.y * 25)) \
                        or wall.hit_box.collidepoint((self.player.rect.centerx + direction.x * 50,
                                                      self.player.rect.centery + direction.y * 50)):
                    bullet_will_not_touch_a_wall = False
            if bullet_will_not_touch_a_wall:
                new_bullet = {
                    'type': self.player.current_gun,
                    'start_pos':
                        (self.player.rect.centerx + direction.x * 50, self.player.rect.centery + direction.y * 50),
                    'start_time': self.time_management.get_game_time(),
                    'direction': (direction.x, direction.y),
                    'speed': velocity_bullet,
                    'damage': damage[self.player.current_gun]
                }
                self.bullets.append(new_bullet)

        self.clear_bullet()

        self.other_player.set_information(self.game_state[self.other_player_count])

        self.text_management.draw_main_room(self.time_management.get_game_time(), self.player)

        self.all_sprites.update(dt, self.time_management.get_game_time(),
                                self.game_state[self.other_player_count]['bullets'])
        self.all_sprites.draw(self.screen)
        self.draw_all_bullet(self.game_state[self.other_player_count]['bullets'])
        self.draw_all_bullet(self.bullets)

        pygame.display.update()

    def waiting_room(self):

        #  --------Background--------
        self.screen.fill('black')

        #  -----------Text-----------     

        self.text_management.draw_waiting_room(pygame.time.get_ticks())

    def clear_border_sprite(self):
        for sprite in self.all_sprites.sprites():
            if hasattr(sprite, 'rect'):
                if sprite.rect.x < -100 or sprite.rect.x > 1050:
                    sprite.kill()
                if sprite.rect.y < -100 or sprite.rect.y > 750:
                    sprite.kill()

        for bullet in self.bullets:
            try:
                if self.time_management.get_game_time() - bullet['start_time'] > 5000:
                    self.bullets.remove(bullet)
            except KeyError:
                pass

    def clear_bullet(self):
        for wall in self.walls:
            for bullet_count, bullet_info in enumerate(self.bullets):
                if wall.hit_box.collidepoint(get_actually_bullet_pos(bullet_info,
                                                                     self.time_management.get_game_time())):
                    del self.bullets[bullet_count]

    def draw_all_bullet(self, bullet_list):
        for bullet in bullet_list:
            draw_bullet(self.screen, bullet, self.time_management.get_game_time())
