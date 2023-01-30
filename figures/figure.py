import pygame

from client.game import game


class Figure:
    def __init__(self, cell, name, img_path, player, winner_mark=False):
        self.name = name
        self.cell = cell
        self.start_cell = cell
        self.player = player
        self.img_path = img_path
        self.can_go_under_attack = not winner_mark
        self.show_attacks = winner_mark
        self.winner_mark = winner_mark

    @property
    def game(self):
        return self.cell.board.game

    @property
    def board(self):
        return self.cell.board

    @property
    def image(self):
        img = pygame.image.load(self.img_path)
        return pygame.transform.scale(img, [self.cell.width * 0.65, self.cell.height * 0.75])

    def can_move_to(self, cell, check_other_figures=True):
        raise NotImplementedError()

    def can_eat_to(self, cell, figure, check_other_figures=True):
        return self.can_move_to(cell, check_other_figures)

    def is_defending(self, cell, check_other_figures=True):
        if cell.figure is None:
            return self.can_eat_to(cell, Figure(cell, 'NULL', '', self.player.other_players[0]), check_other_figures)
        f = cell.figure
        cell.figure = None
        res = self.can_eat_to(cell, Figure(cell, 'NULL', '', f.player.other_players[0]), check_other_figures)
        cell.figure = f
        return res

    def move_to(self, cell, need_to_notify_server=True):
        if need_to_notify_server:
            self.game.record_move(self.cell, cell)
        self.cell.need_redraw = True
        self.cell.figure = None
        if cell.figure is not None:
            game.figure_eaten(cell.figure)
        cell.figure = self
        cell.need_redraw = True
        self.cell = cell

    def __call__(self, **kw):
        cell = kw.get('cell', self.cell)
        if 'cell' in kw:
            kw.pop('cell')
        player = kw.get('player', self.player)
        if 'player_id' in kw:
            kw.pop('player_id')
        return self.__class__(cell=cell, player=player, **kw)

    def can_move_anywhere(self):
        for r in range(self.board.height):
            for c in range(self.board.width):
                cell = self.board.cell(c, r)
                if cell.figure is None and self.can_move_to(cell) or cell.figure is not None and self.can_eat_to(cell):
                    return True
        return False