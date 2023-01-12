from figures.figure import Figure
from game import game


class Camel(Figure):
    def __init__(self, cell, player_id):
        super().__init__(cell, 'Верблюд', f'pics\\camel_{game.get_color(player_id)}.png', player_id)

    def can_move_to(self, cell):
        if (cell is self.cell) or not cell.available_for(self.cell.figure):
            return False

        delta_x = abs(cell.col - self.cell.col)
        delta_y = abs(cell.row - self.cell.row)

        return delta_y == 3 and delta_x == 1 or delta_x == 3 and delta_y == 1
