class Player:
    def __init__(self, id_, image_postfix, other_players):
        self.id = id_
        self.image_postfix = image_postfix
        self.other_players = other_players

    def get_image_name(self, figure_name):
        return f'pics/{figure_name}_{self.image_postfix}.png'

    def __eq__(self, other):
        return self.id == other.id

