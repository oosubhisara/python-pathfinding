
import pygame
from constants import *

class CellPos:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def set(self, row, col):
        self.row = row
        self.col = col

class Cell:
    def __init__(self, row, col):
        self.value = '.'
        self.row = row
        self.col = col

    def draw(self, screen, w, h, color):
        rect = (self.col * CELLSIZE + (CELLSIZE - w) / 2, 
                self.row * CELLSIZE + (CELLSIZE - h) / 2,
                w, h)
        pygame.draw.rect(screen, color, rect)

class Map:
    def __init__(self, rows, cols, cellsize):
        self.row_count = rows
        self.col_count = cols
        self.cellsize = cellsize
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self._start = None
        self._end = None

    def get(self, row, col):
        return self.cells[row][col].value
    
    def set (self, row, col, value):
        if self.cells[row][col].value not in ['S', 'E']:
            self.cells[row][col].value = value

            if value == 'S':
                if self._start is not None:
                    self._start.value = '.'
                self._start = self.cells[row][col]
            elif value == 'E':
                if self._end is not None:
                    self._end.value = '.'
                self._end = self.cells[row][col]

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_start_pos(self):
        return CellPos(self._start.row, self._start.col)

    def get_end_pos(self):
        return CellPos(self._end.row, self._end.col)

    def load(self):
        with open('map.dat', 'r') as f:
            for row in range(self.row_count):
                for col in range(self.col_count):
                    value = f.read(1)  # read one character

                    if value in ['.', 'W', 'S', 'E']:  # valid character
                        if value == 'S':
                            if self._start is not None:
                                self._start.value = '.'
                            self._start = self.cells[row][col]
                            self._start.value = value
                        elif value == 'E':
                            if self._end is not None:
                                self._end.value = '.'
                            self._end = self.cells[row][col]
                            self._end.value = value
                        else:
                            self.cells[row][col].value = value
                    else:
                        self.cells[row][col].value = '.'  # invalid character

                f.read(1)  # discard new line character

    def save(self):
        with open('map.dat', 'w') as f:
            for row in range(self.row_count):
                for col in range(self.col_count):
                    f.write(self.cells[row][col].value)
                f.write('\n')

            print("Saved")

    def draw(self, screen):

        for row in range(self.row_count):
            for col in range(self.col_count):
                cell = self.cells[row][col]

                # Draw floor or wall
                if cell.value == 'W':
                    cell.draw(screen, TILE_SIZE, TILE_SIZE, WALL_COLOR)
                else:
                    cell.draw(screen, TILE_SIZE, TILE_SIZE, FLOOR_COLOR)

                # Draw tile
                if cell.value == 'S':
                    cell.draw(screen, TILE_SIZE - 4, TILE_SIZE - 4,
                              START_COLOR)
                elif cell.value == 'E':
                    cell.draw(screen, TILE_SIZE - 4, TILE_SIZE - 4,
                              END_COLOR)


