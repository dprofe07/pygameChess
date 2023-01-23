from client.player import Player as PlayerClient


class Player(PlayerClient):
    def __init__(self, id_, image_postfix, other_players, user):
        super().__init__(id_, image_postfix, other_players)
        self.user = user

    def get_image_name(self, figure_name):
        return f'pics/{figure_name}_{self.image_postfix}.png'

    def __eq__(self, other):
        return self.id == other.id
