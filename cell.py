import pygame

from constants import WHITE_BOARD, BLACK_BOARD


class Cell:
    def __init__(self, board, row, col):
        self.board = board
        self.row = row
        self.col = col
        self.piece = None

    def get_color(self):
        if (self.row + self.col) % 2 == 0:
            return WHITE_BOARD
        else:
            return BLACK_BOARD
