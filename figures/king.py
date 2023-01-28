from figures.figure import Figure


class King(Figure):
    def __init__(self, cell, player):
        super(King, self).__init__(cell, 'Король', player.get_image_name('king'), player, True)

    def can_move_to(self, cell, check_other_figures=True):
        if not cell.available_for(self, check_other_figures):
            return False

        delta_x = abs(cell.col - self.cell.col)
        delta_y = abs(cell.row - self.cell.row)

        return delta_y < 2 and delta_x < 2

