import sys
import pygame
from config import background, font
from utils import draw_text
import os
pygame.init()


class Settings:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.base_font = pygame.font.Font(None, 32)
        data = open('assets/network/connection.txt')
        # --------Variable In Option--------
        self.port = '9000'
        self.address = '192.168.1.26'

        # --------Rectangle Input--------
        self.port_input_rect = pygame.Rect(200, 200, 140, 32)
        self.address_input_rect = pygame.Rect(200, 300, 140, 32)

        #  Color
        self.color_active = pygame.Color('black')
        self.color_passive = pygame.Color((7, 7, 7))
        self.color = self.color_passive

    def run(self):
        run = True
        input_port_active = False
        input_address_active = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.port_input_rect.collidepoint(event.pos):
                        input_port_active = True
                        input_address_active = False

                    elif self.address_input_rect.collidepoint(event.pos):
                        input_address_active = True
                        input_port_active = False
                    else:
                        input_address_active = False
                        input_port_active = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                    if input_port_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.port = self.port[:-1]
                        elif event.key == pygame.K_RETURN:
                            input_port_active = False
                        else:
                            self.port += event.unicode

                    if input_address_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.address = self.address[:-1]
                        elif event.key == pygame.K_RETURN:
                            input_address_active = False
                        else:
                            self.address += event.unicode

            if input_port_active or input_address_active:
                self.color = self.color_active
            else:
                self.color = self.color_passive

            self.draw()

            pygame.display.flip()

    def draw(self):
        self.screen.blit(background['menu'], background['menu'].get_rect(center=(450, 325)))
        text_port = self.base_font.render(self.port, True, (255, 255, 255))
        text_address = self.base_font.render(self.address, True, (255, 255, 255))

        pygame.draw.rect(self.screen, self.color, self.port_input_rect)
        self.screen.blit(text_port, (self.port_input_rect.x + 5, self.port_input_rect.y + 5))
        self.port_input_rect.w = max(50, text_port.get_width() + 10)

        pygame.draw.rect(self.screen, self.color, self.address_input_rect)
        self.screen.blit(text_address, (self.address_input_rect.x + 5, self.address_input_rect.y + 5))
        self.address_input_rect.w = max(100, text_address.get_width() + 10)

        draw_text('SETTINGS', font['Air'], (255, 255, 255), self.screen, 450, 30, side='center')
