import pygame
from config import speed
from utils import calcul_vector, get_actually_bullet_pos


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.default_image = {}
        self.current_gun = 'gun'
        self.import_animations()

        # General Setup
        self.image = self.default_image[self.current_gun]
        self.rect = self.image.get_rect(center=pos)

        # Movement Attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = speed
        self.angle = 0

        # Collision
        self.hit_box = self.rect.copy().inflate(-64, -64)
        self.collision_sprites = collision_sprites

        # Bullet Attributes
        self.max_bullet = 100
        self.bullet = self.max_bullet
        self.missile_hit_me = []

        # Heal Attribute
        self.heal_max = 50
        self.heal = 50
        self.alive = True

    def import_animations(self):
        for animation in ['run', 'assault rifle', 'gun', 'death']:
            image = pygame.image.load(f'assets/sprites/player/{animation}1.png').convert_alpha()
            image = pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))

            self.default_image[animation] = image

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hit_box'):
                if sprite.hit_box.colliderect(self.hit_box):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hit_box.right = sprite.hit_box.left
                        if self.direction.x < 0:  # moving left
                            self.hit_box.left = sprite.hit_box.right
                        self.rect.centerx = self.hit_box.centerx
                        self.pos.x = self.hit_box.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hit_box.bottom = sprite.hit_box.top
                        if self.direction.y < 0:  # moving up
                            self.hit_box.top = sprite.hit_box.bottom
                        self.rect.centery = self.hit_box.centery
                        self.pos.y = self.hit_box.centery

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_z]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LSHIFT]:
            self.current_gun = 'assault rifle'
        if keys[pygame.K_SPACE]:
            self.current_gun = 'run'
        #  ------------Update Angle------------  #
        vector_direction = calcul_vector(self.pos, pygame.mouse.get_pos())
        self.angle = vector_direction.angle_to((0, 0))

    def update_image(self):
        if self.alive:
            # Image Update
            self.image = pygame.transform.rotate(self.default_image[self.current_gun], self.angle)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.pos.x
            self.rect.centery = self.pos.y

    def set_information(self, game_state):
        self.pos.x = game_state['pos'][0]
        self.pos.y = game_state['pos'][1]
        self.angle = game_state['angle']
        self.current_gun = game_state['current_gun']
        self.heal = game_state['heal_point']

    def set_position(self, position_x, position_y):
        self.hit_box.centerx = round(position_x)
        self.rect.centerx = self.hit_box.centerx

        self.hit_box.centery = round(position_y)
        self.rect.centery = self.hit_box.centery

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed[self.current_gun] * dt
        self.hit_box.centerx = round(self.pos.x)
        self.rect.centerx = self.hit_box.centerx
        self.collision('horizontal')

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed[self.current_gun] * dt
        self.hit_box.centery = round(self.pos.y)
        self.rect.centery = self.hit_box.centery
        self.collision('vertical')

    def check_bullet_hit(self, enemy_bullets, time):
        for bullet in enemy_bullets:
            if self.hit_box.collidepoint(get_actually_bullet_pos(bullet, time)) and not (bullet in self.missile_hit_me):
                self.missile_hit_me.append(bullet)

                self.heal -= bullet['damage']

    def update(self, dt, time, enemy_bullets):
        if self.heal <= 0:
            self.alive = False

        if self.alive:
            self.move(dt)
            self.update_image()
            self.check_bullet_hit(enemy_bullets, time)
        else:
            image = pygame.image.load(
                r'./assets/sprites/player/contour-de-craie-de-cadavre-sur-l-asphalte-27900609.jpg')
            self.image = pygame.transform.scale(image, (75, 75))
            self.rect = self.image.get_rect(center=self.pos)
