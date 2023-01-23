from figures.figure import Figure
from client.game import game


class Pawn(Figure):
    def __init__(self, cell, player, allow_big_step=True):
        super().__init__(cell, 'Пешка', player.get_image_name('pawn'), player)
        self.allow_big_step = allow_big_step

    def can_move_to(self, cell, check_other_figures=True):
        if not cell.available_for(self, check_other_figures):
            return False

        delta_x = abs(self.cell.col - cell.col)
        delta_y = self.cell.row - cell.row
        if delta_x == 0:
            if cell.figure is None:
                if (
                        (delta_y == 1 and self.board.reversed_board == (self.player is self.game.black_player)) or
                        (delta_y == -1 and self.board.reversed_board == (self.player is self.game.white_player))
                ):
                    return True
                elif (
                        (
                                (delta_y == 2 and self.board.reversed_board == (self.player is self.game.black_player)) or
                                (delta_y == -2 and self.board.reversed_board == (self.player is self.game.white_player))
                        ) and
                        self.cell is self.start_cell and
                        self.allow_big_step
                ):
                    return True
        elif delta_x == 1:
            return self.can_eat_to(cell, cell.figure, check_other_figures)
        return False

    def can_eat_to(self, cell, figure, check_other_figures=True):
        if figure is None or not cell.available_for(self, check_other_figures):
            return False

        delta_x = abs(self.cell.col - cell.col)
        delta_y = self.cell.row - cell.row
        if delta_x == 1:
            if (
                    (delta_y == 1 and self.board.reversed_board == (self.player is self.game.black_player)) or
                    (delta_y == -1 and self.board.reversed_board == (self.player is self.game.white_player))
            ):
                return True
        return False

    def __call__(self, **kw):
        cell = kw.get('cell', self.cell)
        if 'cell' in kw:
            kw.pop('cell')
        player = kw.get('player', self.player)
        if 'player_id' in kw:
            kw.pop('player_id')
        allow_big_step = kw.get('allow_big_step', self.allow_big_step)
        if 'allow_big_step' in kw:
            kw.pop('allow_big_step')
        return self.__class__(cell=cell, player=player, allow_big_step=allow_big_step, **kw)
