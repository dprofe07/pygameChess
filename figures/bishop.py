from figures.figure import Figure
from client.game import game


class Bishop(Figure):
    def __init__(self, cell, player):
        super().__init__(cell, 'Слон', player.get_image_name('bishop'), player)

    def can_move_to(self, cell, check_other_figures=True):
        x = self.cell.col
        y = self.cell.row

        if (
                (x - cell.col != y - cell.row and cell.col - x != y - cell.row) or
                (cell is self.cell) or
                not cell.available_for(self, check_other_figures)
        ):
            return False

        if x - cell.col == y - cell.row:
            while x < game.board.width - 1 and y < game.board.height - 1:
                x += 1
                y += 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break

            x = self.cell.col
            y = self.cell.row

            while x > 0 and y > 0:
                x -= 1
                y -= 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break
        elif cell.col - x == y - cell.row:
            x = self.cell.col
            y = self.cell.row

            while x < game.board.width - 1 and y > 0:
                x += 1
                y -= 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break

            x = self.cell.col
            y = self.cell.row

            while x > 0 and y < game.board.height - 1:
                x -= 1
                y += 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break

        return False
