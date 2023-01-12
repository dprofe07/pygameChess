from figures.figure import Figure
from game import game


class Pawn(Figure):
    def __init__(self, cell, player_id, allow_big_step=True):
        super().__init__(cell, 'Пешка', f'pics\\pawn_{game.get_color(player_id)}.png', player_id)
        self.allow_big_step = allow_big_step

    def can_move_to(self, cell):
        if (self.cell is cell) or (not cell.available_for(self)):
            return False

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

    def __call__(self, **kw):
        cell = kw.get('cell', self.cell)
        if 'cell' in kw:
            kw.pop('cell')
        player_id = kw.get('player_id', self.player_id)
        if 'player_id' in kw:
            kw.pop('player_id')
        allow_big_step = kw.get('allow_big_step', self.allow_big_step)
        if 'allow_big_step' in kw:
            kw.pop('allow_big_step')
        return self.__class__(cell=cell, player_id=player_id, allow_big_step=allow_big_step, **kw)
