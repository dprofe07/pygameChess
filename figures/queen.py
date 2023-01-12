from figures.bishop import Bishop
from figures.figure import Figure
from figures.rook import Rook
from game import game


class Queen(Figure):
    def __init__(self, cell, player_id):
        Figure.__init__(self, cell, 'Ферзь', f'pics\\queen_{game.get_color(player_id)}.png', player_id)

    def can_move_to(self, cell):
        # noinspection PyTypeChecker
        return Rook.can_move_to(self, cell) or Bishop.can_move_to(self, cell)