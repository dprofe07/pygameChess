from figures.figure import Figure
from game import game


class Pawn(Figure):
    def __init__(self, cell, player_id, allow_big_step=True):
        super().__init__(cell, 'Пешка', f'pics\\pawn_{game.get_color(player_id)}.png', player_id)
        self.allow_big_step = allow_big_step

    def can_move_to(self, cell):
        delta_x = self.cell.col - cell.col
        delta_y = self.cell.row - cell.row
        if delta_x == 0:
            if cell.figure is None:
                if delta_y == (-1 if (game.black_player == self.player_id) else 1):
                    return True
                elif delta_y == (-2 if (game.black_player == self.player_id) else 2) and self.cell is self.start_cell and self.allow_big_step:
                    return True
        elif delta_x == 1 or delta_x == -1:
            if cell.figure is not None and delta_y == (-1 if (game.black_player == self.player_id) else 1) and cell.figure.player_id != self.player_id:
                return True
        return False
