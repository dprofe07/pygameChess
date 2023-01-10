from figures.figure import Figure
from game import game


class Pawn(Figure):
    def __init__(self, cell, player_id):
        super().__init__(cell, 'Пешка', f'pics\\pawn_{game.get_color(player_id)}.png', player_id)

    def can_move_to(self, cell):
        delta_x = self.cell.col - cell.col
        delta_y = self.cell.row - cell.row
        return delta_x == 0 and delta_y == (-1 if (game.black_player == self.player_id) else 1)
