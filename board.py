import pygame

from cell import Cell
from constants import Colors


class Board:
    def __init__(self, screen, width, height, color=Colors.WHITE, square_cells=False):
        self.screen = screen
        self.width = width
        self.height = height
        self.color = color
        self.square_cells = square_cells

        self.vert_margin = 0
        self.hor_margin = 0
        self.cell_height = 0
        self.cell_width = 0
        self.selected_cell = None

        self.screen_resized()

        self.data = [[Cell(self, y, x) for x in range(self.width)] for y in range(self.height)]

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.hor_margin - 2, self.vert_margin - 2, self.width * self.cell_width + 2 * 2, self.height * self.cell_height + 2 * 2], 2)

        for y in range(self.height):
            for x in range(self.width):
                img = self.cell(x, y).get_image()

                self.screen.blit(
                    img, img.get_rect(
                        topleft=[
                            self.hor_margin + self.cell_width * x,
                            self.vert_margin + self.cell_height * y
                        ]
                    )
                )


    def cell(self, x, y):
        return self.data[y][x]

    def screen_resized(self):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        self.vert_margin = 30
        self.hor_margin = 30

        if self.square_cells and screen_h != screen_w:
            if screen_w > screen_h:
                self.hor_margin += (screen_w - screen_h) // 2
            else:
                self.vert_margin += (screen_h - screen_w) // 2

        self.cell_width = (self.screen.get_width() - self.hor_margin * 2) // self.width
        self.cell_height = (self.screen.get_height() - self.vert_margin * 2) // self.height

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
        return self.cell(col, row)

