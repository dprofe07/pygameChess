from figures.bishop import Bishop
from figures.figure import Figure
from figures.rook import Rook


class Queen(Figure):
    def __init__(self, cell, player):
        Figure.__init__(self, cell, 'Ферзь', player.get_image_name('queen'), player)

    def can_move_to(self, cell, check_other_figures=True):
        # noinspection PyTypeChecker
        return Rook.can_move_to(self, cell, check_other_figures) or Bishop.can_move_to(self, cell, check_other_figures)