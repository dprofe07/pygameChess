class Game:
    def __init__(self):
        self.black_player = 1
        self.white_player = 2

        self.board = None
        self.continue_game = False
        self.hand_figure = None

        self.screen = None

    def set_board(self, board):
        self.board = board

    def run(self):
        if self.board is None:
            print('Can\'t start game, game.board is None')
            return
        if self.screen is None:
            print("Can't start game, game.screen is None")
        self.continue_game = True

    def set_screen(self, screen):
        self.screen = screen

    def stop(self):
        self.continue_game = False

    def get_color(self, player_id):
        return {
            self.white_player: 'white',
            self.black_player: 'black'
        }[player_id]

    def figure_eaten(self, figure):
        pass


game = Game()
