#!/usr/bin/env python3

import pygame
from constants import *
from map import *
from bfs import *
from ui import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption(WINDOW_TITLE)

        self.ui = UI(self.screen)
        self.map = Map(ROWS, COLS, CELLSIZE)

        self.map.load()
        self.path_map = \
                [[PathNode(i, j) for j in range(COLS)] for i in range(ROWS)]
        self.reset_path_map()
        self.path = []
        self.path_speed = PATH_SPEED_1
        self.path_delay = PATH_DELAY_1
        self.path_progress = 0
        self.path_last_time = pygame.time.get_ticks()

    def handle_events(self):
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    return False
                elif key == pygame.K_a:
                    self.ui.previous_tile()
                elif key == pygame.K_d:
                    self.ui.next_tile()
                elif key == pygame.K_w:
                    self.map.save()
                elif key == pygame.K_SPACE:
                    self.find_path()
                elif key == pygame.K_1:
                    self.path_speed = PATH_SPEED_1
                    self.path_delay = PATH_DELAY_1
                    self.ui.set_path_speed(0)
                elif key == pygame.K_2:
                    self.path_speed = PATH_SPEED_2
                    self.path_delay = PATH_DELAY_2
                    self.ui.set_path_speed(1)
                elif key == pygame.K_3:
                    self.path_speed = PATH_SPEED_3
                    self.path_delay = PATH_DELAY_3
                    self.ui.set_path_speed(2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
                if event.button == 1:
                    self.set_cell_value(mouse, TILE_CODES[self.ui.tile_index])
                elif event.button == 3:
                    self.set_cell_value(mouse, TILE_CODES[TILE_EMPTY])
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    self.set_cell_value(mouse, TILE_CODES[self.ui.tile_index])
                elif event.buttons[2]:
                    self.set_cell_value(mouse, TILE_CODES[TILE_EMPTY])

        return True

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.path_last_time > self.path_delay:
            if self.path_progress > 0:
                self.path_progress = self.path_progress + self.path_speed
                if self.path_progress > len(self.path):
                    self.path_progress = len(self.path)
                self.path_last_time = now
            

    def draw(self):
        self.screen.fill((0, 0, 0));
        self.map.draw(self.screen)
        self.draw_path()
        self.ui.draw()

        pygame.display.update()

    def draw_path(self):
        w = CELLSIZE
        h = CELLSIZE
        color = (255, 255, 0)

        pos_index = 0
        for pos in self.path:
            #rect = pygame.Rect(pos.col * CELLSIZE, pos.row * CELLSIZE, w, h)
            #pygame.draw.rect(self.screen, PATH_COLOR_1, rect)
            #rect.inflate_ip(-0.7 * w, -0.7 * h)
            #pygame.draw.rect(self.screen, PATH_COLOR_2, rect)

            cell1 = Cell(pos.row, pos.col)
            cell1.draw(self.screen, TILE_SIZE, TILE_SIZE, PATH_COLOR_1)
            cell2 = Cell(pos.row, pos.col)
            cell2.draw(self.screen, 0.3 * TILE_SIZE, 0.3 * TILE_SIZE, 
                       PATH_COLOR_2)
            pos_index = pos_index + 1
            if pos_index >= self.path_progress:
                break


    def reset_path_map(self):
        for row in range(self.map.row_count):
            for col in range(self.map.col_count):
                self.path_map[row][col].visited = False
                self.path_map[row][col].prev = None
                self.path_map[row][col].walkable = \
                        self.map.get(row, col) != 'W'

    def set_cell_value(self, mouse, value):
        row = int(mouse[1] / CELLSIZE)
        col = int(mouse[0] / CELLSIZE)

        if row < 0 or row > ROWS - 1 or col < 0 or col > COLS - 1:
            return

        self.path = []
        self.map.set(row, col, value)

    def find_path(self):
        self.reset_path_map()
        bfs = Bfs(self.path_map, self.map.row_count, self.map.col_count)
        self.path = bfs.find_path(self.map.get_start_pos(), self.map.get_end_pos())
        self.reset_path_map()

        if len(self.path) > 0:
            print("Path:")
            for pos in self.path:
                print("{0},{1}".format(pos.row, pos.col))

            print(f"Distance: {len(self.path)}")

            self.path_progress = 1
        else:
            print("Path not found.")

def main():
    g = Game()
    clock = pygame.time.Clock()

    while g.handle_events():
        g.update()
        g.draw()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
