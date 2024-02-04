import sys
import pygame
from level import Level
from config import background, button
from settings import Settings
from information_panel import GameText


class Game:
    def __init__(self):

        self.screen_width = 900
        self.screen_height = 650

        self.texts = GameText()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Shooter Game')

        self.clock = pygame.time.Clock()

    def run(self):
        setting = Settings()
        # Main menu display window, graphics to be reviewed...
        while True:
            self.screen.blit(background['menu'], background['menu'].get_rect(center=(450, 325)))

            self.screen.blit(button['blue'], button['blue'].get_rect(center=(500, 230)))          
            self.screen.blit(button['dark blue'], button['dark blue'].get_rect(center=(497, 360)))
            
            self.texts.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button['blue'].get_rect(center=(500, 230)).collidepoint(pygame.mouse.get_pos()):
                            Level(setting).run()
                        if button['dark blue'].get_rect(center=(497, 360)).collidepoint(pygame.mouse.get_pos()):
                            setting.run()

            pygame.display.update()
            self.clock.tick(5)


if __name__ == '__main__':
    pygame.init()
    Game().run()
