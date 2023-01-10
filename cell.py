import pygame

from constants import WHITE_BOARD, BLACK_BOARD, COLOR_CAN_GO


class Cell:
    def __init__(self, board, row, col):
        self.board = board
        self.row = row
        self.col = col
        self.figure = None

    def get_image(self):
        surf = pygame.surface.Surface((self.board.cell_width, self.board.cell_height))
        if (self.row + self.col) % 2 == 0:
            surf.fill(WHITE_BOARD)
        else:
            surf.fill(BLACK_BOARD)
        if self.figure is not None:
            surf.blit(self.figure.image, self.figure.image.get_rect(center=[surf.get_width() // 2, surf.get_height() // 2]))

        if self.board.selected_cell is not None:
            sel_cell = self.board.cell(*self.board.selected_cell)
            if sel_cell.figure is not None and sel_cell.figure.can_move_to(self):
                pygame.draw.circle(surf, COLOR_CAN_GO, [surf.get_width() //2, surf.get_height() // 2], surf.get_width() // 4)
        return surf

    @property
    def width(self):
        return self.board.cell_width

    @property
    def height(self):
        return self.board.cell_height

    def set_figure(self, figure):
        self.figure = figure
