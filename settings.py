import sys
import pygame
import os.path
from information_panel import SettingsText


pygame.init()


class Settings:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.base_font = pygame.font.Font(None, 32)

        if os.path.exists('./connection'):
            file = open('./connection', 'r')
            data = (file.read()).split("|")
            self.address = data[0]
            self.port = data[1]
            file.close()
        else:
            self.address = '192.168.1.26'
            self.port = '9000'

        # ------Text For Variable--------
        self.text_management = SettingsText(self.screen)

        self.clock = pygame.time.Clock()

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
                    if self.text_management.input_rectangles['Address'].collidepoint(event.pos):
                        input_address_active = True
                        input_port_active = False
                    elif self.text_management.input_rectangles['Port'].collidepoint(event.pos):
                        input_address_active = False
                        input_port_active = True
                    else:
                        input_address_active = False
                        input_port_active = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                    if input_port_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.port = self.port[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            input_port_active = False
                        else:
                            self.port += event.unicode

                    if input_address_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.address = self.address[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            input_address_active = False
                        else:
                            self.address += event.unicode

            self.text_management.update(self.address, self.port, input_address_active, input_port_active)
            self.draw()

            self.clock.tick(20)

            pygame.display.flip()

        file = open('./connection', 'w')
        file.write(f'{self.address}|{self.port}')

    def draw(self):
        self.text_management.draw()

        
