import pygame
from utils import calcul_vector

gun = pygame.image.load('assets/sprites/bullet/Bullet.png')
assault_rifle = pygame.image.load('assets/sprites/bullet/BulletProjectile.png')


def draw_bullet(screen, bullet_info, time):
    vector_direction = calcul_vector((0, 0), bullet_info['direction'])

    image = pygame.transform.rotate(eval(bullet_info['type'].replace(' ', '_')).copy(),
                                    vector_direction.angle_to((0, 0)) + 270)
    rect = image.get_rect()

    rect.centerx = bullet_info['start_pos'][0] + bullet_info['direction'][0] * bullet_info['speed'] * (
            (time - bullet_info['start_time']) / 1000.)

    rect.centery = bullet_info['start_pos'][1] + bullet_info['direction'][1] * bullet_info['speed'] * (
            (time - bullet_info['start_time']) / 1000.)

    screen.blit(image, rect)
