import pygame
from config import icon
from config import font


class Text:
    def __init__(self, text, font_family, color, pos, side='topleft'):
        self.text = text
        self.font = font_family
        self.color = color
        self.pos = pos
        self.side = side

        self.text_obj = font_family.render(self.text, 1, self.color)
        self.text_rect = self.text_obj.get_rect()
        setattr(self.text_rect, self.side, self.pos)

    def update_text(self, text):
        self.text = text
        self.text_obj = self.font.render(self.text, 1, self.color)
        self.text_rect = self.text_obj.get_rect()
        setattr(self.text_rect, self.side, self.pos)

    def draw(self, surface):
        surface.blit(self.text_obj, self.text_rect)


class LifeBar:
    def __init__(self, player, pos):
        self.player = player
        self.pos = pos
        self.divisive = 5
        self.heart_type = self.get_heart_type()

        #  Heart icon management
        self.heart_icon = pygame.transform.scale(icon['Health'][self.heart_type].copy(), (30, 30))
        self.heart_icon__rect = self.heart_icon.get_rect(center=pos)

        #  Heart bar background management
        self.heal_max_bar = pygame.Surface((player.heal_max * 5, 34))
        self.heal_max_bar.fill((20, 20, 20))
        self.heal_max_bar_rect = self.heal_max_bar.get_rect(center=pos)

        #  Heart bar management
        self.heal_bar = pygame.Surface((player.heal * 5, 34))
        self.heal_bar.fill('red')
        self.heal_bar_rect = self.heal_bar.get_rect()
        self.heal_bar_rect.topleft = self.heal_max_bar_rect.topleft

    def get_heart_type(self):
        if self.player.heal <= 0:
            heart_icon_type = 'Empty'
        elif (self.player.heal_max / 2) >= self.player.heal:
            heart_icon_type = 'Half'
        else:
            heart_icon_type = 'Total'

        return heart_icon_type

    def update_variable(self, player):
        #  Heart icon management
        self.heart_icon = pygame.transform.scale(icon['Health'][self.heart_type].copy(), (30, 30))
        self.heart_icon__rect = self.heart_icon.get_rect(center=self.pos)

        #  Heart bar management
        if not player.heal <= 0:
            self.heal_bar = pygame.Surface((player.heal * 5, 34))
            self.heal_bar.fill('red')
        
        self.heal_bar_rect = self.heal_bar.get_rect()
        self.heal_bar_rect.topleft = self.heal_max_bar_rect.topleft

    def draw(self, surface):
        surface.blit(self.heal_max_bar, self.heal_max_bar_rect)
        if not self.player.heal <= 0:
            surface.blit(self.heal_bar, self.heal_bar_rect)
        surface.blit(self.heart_icon, self.heart_icon__rect)


class GameText:
    def __init__(self) -> None:
        self.constant_texts = [
            Text('[SHOOTER GAME]', font['Air'], (255, 255, 255), (450, 30), side='center'),
            Text('play', font['Air'], (255, 255, 255), (500, 234), side='center'),
            Text('settings', font['Air'], (255, 255, 255), (497, 362), side='center')
        ]

    def draw(self, screen):
        for text in self.constant_texts:
            text.draw(screen)


class LevelInformationDraw:
    def __init__(self, screen, player, network):
        self.screen = screen
        self.player = player
        self.network = network
        
        #  Text and Heal Bar
        self.constant_texts_waiting_room = [
            Text(f'{str(self.network.addr[0])} | {str(self.network.addr[1])}', font['Times New Roman'], 'white',
                 ((self.screen.get_width()) - 5, self.screen.get_height() - 5), side='bottomright')
            ]

        self.constant_texts_main_room = [

        ]
        
        self.mutable_texts_waiting_room = {
            'Waiting': Text(None, font['Helvetica Grass'], 'red', ((self.screen.get_width() - 268) // 2, 30)),
            }

        self.mutable_texts_main_room = {
            'Time': Text(None, font['News701 BT'], 'green', (20, 20)),
            'HealBar': LifeBar(self.player, (self.screen.get_width() / 2, 20))
            }
        
    def draw_main_room(self, time, player):
        self.screen.fill('black')

        self.mutable_texts_main_room['Time'].update_text(f'{int(time/1000)}s')
        self.mutable_texts_main_room['HealBar'].update_variable(player)
        
        for text in self.constant_texts_main_room:
            text.draw(self.screen)

        for key in self.mutable_texts_main_room.keys():
            self.mutable_texts_main_room[key].draw(self.screen)

    def draw_waiting_room(self, ticks):
        self.mutable_texts_waiting_room['Waiting'].update_text(f"Waiting for Player{int(ticks / 250 % 4) * '.'}")

        for text in self.constant_texts_waiting_room:
            text.draw(self.screen)
        
        for key in self.mutable_texts_waiting_room.keys():
            self.mutable_texts_waiting_room[key].draw(self.screen)


class SettingsText:
    def __init__(self, screen):
        self.screen = screen

        self.settings_bg = pygame.image.load('./assets/background/settings_bg.png')
        self.settings_bg_rect = self.settings_bg.get_rect(
            center=(self.screen.get_width()/2, self.screen.get_height()/2 + 20))

        self.font_input = pygame.font.Font(None, 32)

        self.input_rectangles = {'Address': pygame.Rect(713, 130, 140, 32), 'Port': pygame.Rect(713, 180, 140, 32)}

        self.default_colors = {'Passive': pygame.Color((7, 7, 7)), 'Active': pygame.Color((25, 25, 25))}

        self.colors = {'Address': self.default_colors['Passive'], 'Port': self.default_colors['Passive'], }

        self.constant_texts = [
            Text('SETTINGS', font['Air'], (255, 255, 255), (450, 30), side='center'),
            Text('IP Address: ', font['Settings_font'], (255, 255, 255), (200, 130)),
            Text('Port Number: ', font['Settings_font'], (255, 255, 255), (200, 180)),
        ]
        
        self.mutable_text = {}

        self.text_port = None
        self.text_address = None

    def update(self, address, port, input_address_active, input_port_active):
        self.text_address = self.font_input.render(address, True, (255, 255, 255))
        self.text_port = self.font_input.render(port, True, (255, 255, 255))

        if input_port_active:
            self.colors['Address'] = self.default_colors['Passive']
            self.colors['Port'] = self.default_colors['Active']
        elif input_address_active:
            self.colors['Address'] = self.default_colors['Active']
            self.colors['Port'] = self.default_colors['Passive']
        else:
            self.colors['Address'] = self.default_colors['Passive']
            self.colors['Port'] = self.default_colors['Passive']

    def draw(self):
        self.screen.fill((25, 25, 25))
        self.screen.blit(self.settings_bg, self.settings_bg_rect)

        pygame.draw.rect(self.screen, self.colors['Address'], self.input_rectangles['Address'])
        self.screen.blit(self.text_address,
                         (self.input_rectangles['Address'].x + 5, self.input_rectangles['Address'].y + 5))
        self.input_rectangles['Address'].w = max(137, self.text_address.get_width() + 10)
        self.input_rectangles['Address'].topright = (713, 130 + 15)

        pygame.draw.rect(self.screen, self.colors['Port'], self.input_rectangles['Port'])
        self.screen.blit(self.text_port, (self.input_rectangles['Port'].x + 5, self.input_rectangles['Port'].y + 5))
        self.input_rectangles['Port'].w = max(137, self.text_port.get_width() + 10)
        self.input_rectangles['Port'].topright = (713, 180 + 15)

        for text in self.constant_texts:
            text.draw(self.screen)
            