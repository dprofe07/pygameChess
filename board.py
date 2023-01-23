import pygame

from cell import Cell
from constants import Colors
from figures import Queen, Bishop, Rook, Pawn, King, Knight, Camel, GrassHopper


class Board:
    def __init__(self, game, screen, width, height, color=Colors.WHITE, square_cells=False, reversed_board=False):
        self.reversed_board = reversed_board
        self.configs = {
            'std': [
                [
                    Rook(None, game.black_player),
                    Knight(None, game.black_player),
                    Bishop(None, game.black_player),
                    Queen(None, game.black_player),
                    King(None, game.black_player),
                    Bishop(None, game.black_player),
                    Knight(None, game.black_player),
                    Rook(None, game.black_player)
                ],
                [Pawn(None, game.black_player)] * 8,
                [None] * 8,
                [None] * 8,
                [None] * 8,
                [None] * 8,
                [Pawn(None, game.white_player)] * 8,
                [
                    Rook(None, game.white_player),
                    Knight(None, game.white_player),
                    Bishop(None, game.white_player),
                    Queen(None, game.white_player),
                    King(None, game.white_player),
                    Bishop(None, game.white_player),
                    Knight(None, game.white_player),
                    Rook(None, game.white_player)
                ],
            ],

            '+camel': [
                [
                    Rook(None, game.black_player),
                    Knight(None, game.black_player),
                    Camel(None, game.black_player),
                    Bishop(None, game.black_player),
                    Queen(None, game.black_player),
                    King(None, game.black_player),
                    Bishop(None, game.black_player),
                    Camel(None, game.black_player),
                    Knight(None, game.black_player),
                    Rook(None, game.black_player)
                ],
                [Pawn(None, game.black_player)] * 10,
                [None] * 10,
                [None] * 10,
                [None] * 10,
                [None] * 10,
                [None] * 10,
                [None] * 10,
                [Pawn(None, game.white_player)] * 10,
                [
                    Rook(None, game.white_player),
                    Knight(None, game.white_player),
                    Camel(None, game.white_player),
                    Bishop(None, game.white_player),
                    Queen(None, game.white_player),
                    King(None, game.white_player),
                    Bishop(None, game.white_player),
                    Camel(None, game.white_player),
                    Knight(None, game.white_player),
                    Rook(None, game.white_player)
                ],
            ],
            '+camel+grasshopper': [
                [
                    Rook(None, game.black_player),
                    Knight(None, game.black_player),
                    Camel(None, game.black_player),
                    Bishop(None, game.black_player),
                    GrassHopper(None, game.black_player),
                    Queen(None, game.black_player),
                    King(None, game.black_player),
                    GrassHopper(None, game.black_player),
                    Bishop(None, game.black_player),
                    Camel(None, game.black_player),
                    Knight(None, game.black_player),
                    Rook(None, game.black_player)
                ],
                [Pawn(None, game.black_player)] * 12,
                [None] * 12,
                [None] * 12,
                [None] * 12,
                [None] * 12,
                [Pawn(None, game.white_player)] * 12,
                [
                    Rook(None, game.white_player),
                    Knight(None, game.white_player),
                    Camel(None, game.white_player),
                    Bishop(None, game.white_player),
                    GrassHopper(None, game.white_player),
                    Queen(None, game.white_player),
                    King(None, game.white_player),
                    GrassHopper(None, game.white_player),
                    Bishop(None, game.white_player),
                    Camel(None, game.white_player),
                    Knight(None, game.white_player),
                    Rook(None, game.white_player)
                ],
            ],

            'mini': [
                [Rook(None, game.black_player), Bishop(None, game.black_player), King(None, game.black_player),
                 Bishop(None, game.black_player), Rook(None, game.black_player)],
                [Pawn(None, game.black_player)] * 5,
                [None] * 5,
                [None] * 5,
                [None] * 5,
                [None] * 5,
                [Pawn(None, game.white_player)] * 5,
                [Rook(None, game.white_player), Bishop(None, game.white_player), King(None, game.white_player),
                 Bishop(None, game.white_player), Rook(None, game.white_player)],
            ],
            'test': [
                [None, None, None, None, Pawn(None, game.black_player)],
                [None] * 5,
                [None, None, King(None, game.white_player), None, None],
                [None] * 5,
                [None] * 5,
            ]

        }

        self.screen = screen
        self.width = width
        self.height = height
        self.color = color
        self.square_cells = square_cells
        self.game = game

        self.vert_margin = 0
        self.hor_margin = 0
        self.cell_height = 0
        self.cell_width = 0
        self.selected_cell = None

        self.data = []

        self.screen_resized(True)

    def put_figure(self, figure):
        figure.cell.figure = figure

    def load_config(self, name):
        if name not in self.configs:
            return self.configs[name]

        self.height = len(self.configs[name])
        if self.height > 0:
            self.width = len(self.configs[name][0])
        else:
            self.width = 0

        self.screen_resized(True)

        if not self.reversed_board:
            for r in range(len(self.configs[name])):
                for c in range(len(self.configs[name][r])):
                    if self.configs[name][r][c] is not None:
                        self.put_figure(self.configs[name][r][c](cell=self.cell(c, r)))
        else:
            for r in range(self.height):
                for c in range(self.width):
                    if self.configs[name][r][c] is not None:
                        self.put_figure(self.configs[name][r][c](cell=self.cell(self.width - c - 1, self.height - r - 1)))

    def draw(self, mouse_pos):
        pygame.draw.rect(
            self.screen, self.color,
            [
                self.hor_margin - 2, self.vert_margin - 2,
                self.width * self.cell_width + 2 * 2, self.height * self.cell_height + 2 * 2
            ],
            2
        )

        curr_cell = self.cell_by_coords(mouse_pos)

        for y in range(self.height):
            for x in range(self.width):
                img = self.cell(x, y).get_image(curr_cell, self.reversed_board)

                self.screen.blit(
                    img, img.get_rect(
                        topleft=[
                            self.hor_margin + self.cell_width * x,
                            self.vert_margin + self.cell_height * y
                        ]
                    )
                )

    def cell(self, x, y):
        # print(x, y)
        return self.data[y][x]

    def screen_resized(self, clear_data=False):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        self.vert_margin = 30
        self.hor_margin = 30

        self.cell_width = (self.screen.get_width() - self.hor_margin * 2) // self.width
        self.cell_height = (self.screen.get_height() - self.vert_margin * 2) // self.height

        if self.square_cells:
            if self.cell_width > self.cell_height:
                self.cell_width = self.cell_height
                self.hor_margin = (screen_w - self.cell_width * self.width) // 2
            else:
                self.cell_height = self.cell_width
                self.vert_margin = (screen_h - self.cell_height * self.height) // 2

        if clear_data:
            self.data = [[Cell(self, y, x) for x in range(self.width)] for y in range(self.height)]

    def cell_by_coords(self, coords):
        if (
                coords[0] < self.hor_margin or
                coords[1] < self.vert_margin or
                coords[0] > self.hor_margin + (self.width * self.cell_width) or
                coords[1] > self.vert_margin + (self.height * self.cell_height)
        ):
            return None
        col = (coords[0] - self.hor_margin) // self.cell_width
        row = (coords[1] - self.vert_margin) // self.cell_height
        if col >= self.width or row >= self.height:
            return None
        return self.cell(col, row)
