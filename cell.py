import pygame

from constants import WHITE_BOARD, BLACK_BOARD, SELECTED_BOARD, DROP_BOARD, CAN_MOVE_TO_BOARD


class Cell:
    def __init__(self, board, row, col):
        self.board = board
        self.row = row
        self.col = col
        self.figure = None

    @property
    def game(self):
        return self.board.game

    def available_for(self, figure, check_other_figures=True):
        if self.figure is not None and self.figure.player == figure.player:
            return False

        if check_other_figures:
            if not figure.can_go_under_attack and self.attacked_by(figure.player.other_players[0]):
                return False

        if self.figure is None or self.figure.player is not figure.player:
            return True
        return False

    def attacked_by(self, player):
        for i in self.game.board.data:
            for j in i:
                if j.figure is not None:
                    if j.figure.player is player and j.figure.is_defending(self, False):
                        return True
        return False

    def get_image(self, curr_cell, board_reversed=False):
        surf = pygame.surface.Surface((self.board.cell_width, self.board.cell_height))
        sh = surf.get_height()
        sw = surf.get_width()

        if ((self.row + self.col) % 2 == int(board_reversed)) or ((self.row + self.col) % 2 == int(board_reversed)):
            surf.fill(WHITE_BOARD)
        else:
            surf.fill(BLACK_BOARD)

        if self.figure is not None and self.figure.show_attacks and self.attacked_by(self.game.other_player(self.figure.player)):
            pygame.draw.circle(surf, [255, 0, 0], [sw // 2, sh // 2], sw // 5 * 2.5)

        if self.game.hand_figure is not None and curr_cell is not None:
            if self is curr_cell and self.game.hand_figure.can_move_to(self):
                surf.fill(DROP_BOARD)

        if self.board.selected_cell is not None:
            if (
                    (self.board.selected_cell.figure is not None and self.board.selected_cell.figure.can_move_to(self)) or
                    (self.game.hand_figure is not None and self.game.hand_figure.can_move_to(self))
            ):
                if self.figure is None:
                    pygame.draw.circle(surf, CAN_MOVE_TO_BOARD, [sw // 2, sh // 2], sw // 7)
                else:
                    pygame.draw.polygon(surf, CAN_MOVE_TO_BOARD, [(0, 0), (sw // 5, 0), (0, sh // 5)])
                    pygame.draw.polygon(surf, CAN_MOVE_TO_BOARD, [(0, sh), (sw // 5, sh), (0, sh // 5 * 4)])
                    pygame.draw.polygon(surf, CAN_MOVE_TO_BOARD, [(sw, 0), (sw // 5 * 4, 0), (sw, sh // 5)])
                    pygame.draw.polygon(surf, CAN_MOVE_TO_BOARD, [(sw, sh), (sw // 5 * 4, sh), (sw, sh // 5 * 4)])

            if self.board.selected_cell is self:
                surf.fill(SELECTED_BOARD)

        if self.figure is not None:
            surf.blit(self.figure.image, self.figure.image.get_rect(center=[sw // 2, sh // 2]))

        return surf

    @property
    def width(self):
        return self.board.cell_width

    @property
    def height(self):
        return self.board.cell_height

    def set_figure(self, figure):
        self.figure = figure

    def coords(self):
        return self.col, self.row
