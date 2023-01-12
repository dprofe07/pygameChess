import pygame

from game import game


class Figure:
    def __init__(self, cell, name, img_path, player_id):
        self.name = name
        self.cell = cell
        self.start_cell = cell
        self.player_id = player_id
        self.img_path = img_path

    @property
    def image(self):
        img = pygame.image.load(self.img_path)

        return pygame.transform.scale(img, [self.cell.width * 0.9, self.cell.height * 0.9])

    def can_move_to(self, cell):
        raise NotImplementedError()

    def move_to(self, cell):
        self.cell.figure = None
        if cell.figure is not None:
            game.figure_eaten(cell.figure)
        cell.figure = self
        self.cell = cell

    def __call__(self, **kw):
        cell = kw.get('cell', self.cell)
        if 'cell' in kw:
            kw.pop('cell')
        player_id = kw.get('player_id', self.player_id)
        if 'player_id' in kw:
            kw.pop('player_id')
        return self.__class__(cell=cell, player_id=player_id, **kw)
