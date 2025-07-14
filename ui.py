import pygame
from constants import *

class Text:
    def __init__(self, caption, font, x, y, color):
        self.caption = caption
        self.x = x
        self.y = y
        self.surface = font.render(self.caption, True, color)
        rect = self.surface.get_rect()
        self.rect = pygame.Rect(x, y, rect.w, rect.h)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.tile_index = TILE_WALL

        self.font = pygame.font.SysFont('sans', 16)

        self.x = 16
        self.status_texts = ["", ""]
        self.status_texts[0] = Text("Tile: ", self.font, self.x, 0, SILVER)
        self.line_height = self.status_texts[0].rect.h + 20
        self.y = WINDOW_H - (2 * self.line_height) 
        self.status_texts[0].rect.y = self.y

        self.tile_texts = [
                Text("Empty", self.font, self.x, self.y, SILVER),
                Text("Wall", self.font, self.x, self.y, SILVER),
                Text("Start", self.font, self.x, self.y, SILVER),
                Text("End", self.font, self.x, self.y, SILVER),
        ]

        self.hilights = []

        HORIZONTAL_SPACING = 32
        x = self.x + self.status_texts[0].rect.w + HORIZONTAL_SPACING
        for text in self.tile_texts:
            # Reposition tile texts
            text.rect.x = x

            # set hilight rect
            hilight_rect = pygame.Rect(text.rect.x - 10, text.rect.y, 
                                       text.rect.w + 20, text.rect.h)
            self.hilights.append(hilight_rect)
            x = x + text.rect.w + HORIZONTAL_SPACING

        self.tile_index = TILE_WALL
        
        self.path_speed = 0
        x = 680
        self.speed_texts = [
                Text("Speed: Full", self.font, x, self.y, SPEED_COLOR),
                Text("Speed: Fast", self.font, x, self.y, SPEED_COLOR),
                Text("Speed: Slow", self.font, x, self.y, SPEED_COLOR),
        ]

        TILE_SAPARATOR = 10 * " "
        self.status_texts[1] = Text(
                "[A] / [D] = Select tile" + TILE_SAPARATOR +
                "[Mouse] = Draw / Erase" + TILE_SAPARATOR +
                "[W] = Save        " + TILE_SAPARATOR +
                "[SPACE] = Start", 
                self.font, self.x, self.y + self.line_height, SILVER)

    def draw(self):
        self.status_texts[0].draw(self.screen)
        self.status_texts[1].draw(self.screen)

        pygame.draw.rect(self.screen, HILIGHT_COLOR, 
                         self.hilights[self.tile_index])

        for text in self.tile_texts:
            text.draw(self.screen)

        self.speed_texts[self.path_speed].draw(self.screen)

    def previous_tile(self):
        self.tile_index = (self.tile_index - 1) % TILE_COUNT

    def next_tile(self):
        self.tile_index = (self.tile_index + 1) % TILE_COUNT

    def set_path_speed(self, speed):
        self.path_speed = speed
