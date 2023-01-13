from figures.figure import Figure
from game import game


class GrassHopper(Figure):
    def __init__(self, cell, player_id):
        super().__init__(cell, 'Кузнечик', f'pics\\grasshopper_{game.get_color(player_id)}.png', player_id)

    def can_move_to(self, cell):
        if (cell is self.cell) or not cell.available_for(self):
            return False

        delta_x = abs(cell.col - self.cell.col)
        delta_y = abs(cell.row - self.cell.row)

        return delta_y == 2 and delta_x == 0 or delta_y == 0 and delta_x == 2