import pygame

from constants import WHITE_BOARD, BLACK_BOARD, COLOR_CAN_GO, SELECTED_BOARD, DROP_BOARD
from game import game


class Cell:
    def __init__(self, board, row, col):
        self.board = board
        self.row = row
        self.col = col
        self.figure = None

    def available_for(self, figure):
        return (self.figure is None) or (self.figure.player_id != figure.player_id)

    def get_image(self, curr_cell):
        surf = pygame.surface.Surface((self.board.cell_width, self.board.cell_height))

        if (self.row + self.col) % 2 == 0:
            surf.fill(WHITE_BOARD)
        else:
            surf.fill(BLACK_BOARD)

        if game.hand_figure is not None and curr_cell is not None:
            if self is curr_cell:
                surf.fill(DROP_BOARD)

        if self.board.selected_cell is not None:
            sel_cell = self.board.cell(*self.board.selected_cell)
            if sel_cell.figure is not None and sel_cell.figure.can_move_to(self):
                if self.figure is None:
                    pygame.draw.circle(surf, COLOR_CAN_GO, [surf.get_width() // 2, surf.get_height() // 2], surf.get_width() // 4)
                else:
                    pygame.draw.polygon(surf, COLOR_CAN_GO, [(0, 0), (surf.get_width() // 5, 0), (0, surf.get_height() // 5)])
                    pygame.draw.polygon(surf, COLOR_CAN_GO, [(0, surf.get_height()), (surf.get_width() // 5, surf.get_height()), (0, surf.get_height() // 5 * 4)])
                    pygame.draw.polygon(surf, COLOR_CAN_GO, [(surf.get_width(), 0), (surf.get_width() // 5 * 4, 0), (surf.get_width(), surf.get_height() // 5)])
                    pygame.draw.polygon(surf, COLOR_CAN_GO, [(surf.get_width(), surf.get_height()), (surf.get_width() // 5 * 4, surf.get_height()), (surf.get_height(), surf.get_height() // 5 * 4)])
            elif game.hand_figure is not None:
                if game.hand_figure.can_move_to(self):
                    if self.figure is None:
                        pygame.draw.circle(surf, COLOR_CAN_GO, [surf.get_width() // 2, surf.get_height() // 2],
                                           surf.get_width() // 4)
                    else:
                        pygame.draw.polygon(surf, COLOR_CAN_GO,
                                            [(0, 0), (surf.get_width() // 5, 0), (0, surf.get_height() // 5)])
                        pygame.draw.polygon(surf, COLOR_CAN_GO,
                                            [(0, surf.get_height()), (surf.get_width() // 5, surf.get_height()),
                                             (0, surf.get_height() // 5 * 4)])
                        pygame.draw.polygon(surf, COLOR_CAN_GO, [(surf.get_width(), 0), (surf.get_width() // 5 * 4, 0),
                                                                 (surf.get_width(), surf.get_height() // 5)])
                        pygame.draw.polygon(surf, COLOR_CAN_GO, [(surf.get_width(), surf.get_height()),
                                                                 (surf.get_width() // 5 * 4, surf.get_height()),
                                                                 (surf.get_height(), surf.get_height() // 5 * 4)])

            if sel_cell is self:
                surf.fill(SELECTED_BOARD)
        if self.figure is not None:
            surf.blit(self.figure.image, self.figure.image.get_rect(center=[surf.get_width() // 2, surf.get_height() // 2]))

        return surf

    @property
    def width(self):
        return self.board.cell_width

    @property
    def height(self):
        return self.board.cell_height

    def set_figure(self, figure):
        self.figure = figure
