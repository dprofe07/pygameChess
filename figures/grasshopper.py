from figures.figure import Figure


class GrassHopper(Figure):
    def __init__(self, cell, player):
        super().__init__(cell, 'Кузнечик', player.get_image_name('grasshopper'), player)

    def can_move_to(self, cell, check_other_figures=True):
        if (cell is self.cell) or not cell.available_for(self, check_other_figures):
            return False

        delta_x = abs(cell.col - self.cell.col)
        delta_y = abs(cell.row - self.cell.row)

        return delta_y == 2 and delta_x == 0 or delta_y == 0 and delta_x == 2
