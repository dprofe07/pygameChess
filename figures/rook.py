from figures.figure import Figure
from game import game


class Rook(Figure):
    def __init__(self, cell, player_id):
        super().__init__(cell, 'Ладья', f'pics\\rook_{game.get_color(player_id)}.png', player_id)

    def can_move_to(self, cell):
        x = self.cell.col
        y = self.cell.row

        if (
                (x != cell.col and y != cell.row) or
                (cell is self.cell) or
                not cell.available_for(self.cell.figure)
        ):
            return False

        if x == cell.col:
            while y < 7:
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
            while x < 7:
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
