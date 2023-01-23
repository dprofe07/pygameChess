from figures.figure import Figure
from client.game import game


class Rook(Figure):
    def __init__(self, cell, player):
        super().__init__(cell, 'Ладья', player.get_image_name('rook'), player)

    def can_move_to(self, cell, check_other_figures=True):
        x = self.cell.col
        y = self.cell.row

        if not cell.available_for(self, check_other_figures):
            return False

        if x == cell.col:
            while y < game.board.height - 1:
                y += 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break

            y = self.cell.row

            while y > 0:
                y -= 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break
        elif y == cell.row:
            while x < game.board.width - 1:
                x += 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break

            x = self.cell.col

            while x > 0:
                x -= 1
                if cell.col == x and cell.row == y:
                    return True
                if game.board.cell(x, y).figure is not None:
                    break
        return False
