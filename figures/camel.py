from figures.figure import Figure


class Camel(Figure):
    def __init__(self, cell, player):
        super().__init__(cell, 'Верблюд', player.get_image_name('camel'), player)

    def can_move_to(self, cell, check_other_figures=True):
        if (cell is self.cell) or not cell.available_for(self, check_other_figures):
            return False

        delta_x = abs(cell.col - self.cell.col)
        delta_y = abs(cell.row - self.cell.row)

        return delta_y == 3 and delta_x == 1 or delta_x == 3 and delta_y == 1
