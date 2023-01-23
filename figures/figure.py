import pygame

from client.game import game


class Figure:
    def __init__(self, cell, name, img_path, player, can_go_under_attack=True, show_attacks=False):
        self.name = name
        self.cell = cell
        self.start_cell = cell
        self.player = player
        self.img_path = img_path
        self.can_go_under_attack = can_go_under_attack
        self.show_attacks = show_attacks

    @property
    def game(self):
        return self.cell.board.game

    @property
    def board(self):
        return self.cell.board

    @property
    def image(self):
        img = pygame.image.load(self.img_path)

        return pygame.transform.scale(img, [self.cell.width * 0.9, self.cell.height * 0.9])

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
        self.cell.figure = None
        if cell.figure is not None:
            game.figure_eaten(cell.figure)
        cell.figure = self
        self.cell = cell

    def __call__(self, **kw):
        cell = kw.get('cell', self.cell)
        if 'cell' in kw:
            kw.pop('cell')
        player = kw.get('player', self.player)
        if 'player_id' in kw:
            kw.pop('player_id')
        return self.__class__(cell=cell, player=player, **kw)
