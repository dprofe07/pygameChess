from figures.figure import Figure
from game import game


class Bishop(Figure):
    def __init__(self, cell, player_id):
        super().__init__(cell, 'Слон', f'pics\\bishop_{game.get_color(player_id)}.png', player_id)

    def can_move_to(self, cell):
        x = self.cell.col
        y = self.cell.row

        if (
                (x - cell.col != y - cell.row and cell.col - x != y - cell.row) or
                (cell is self.cell) or
                (cell.figure is not None and cell.figure.player_id == self.player_id)
        ):
            return False

        while x < 7 and y < 7:
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

        x = self.cell.col
        y = self.cell.row

        while x < 7 and y > 0:
            x += 1
            y -= 1
            if cell.col == x and cell.row == y:
                return True
            if game.board.cell(x, y).figure is not None:
                break

        x = self.cell.col
        y = self.cell.row

        while x > 0 and y < 7:
            x -= 1
            y += 1
            if cell.col == x and cell.row == y:
                return True
            if game.board.cell(x, y).figure is not None:
                break

        return False
