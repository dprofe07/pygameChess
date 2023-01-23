from player import Player
from client.socket_client import SocketClient
from socket_toolkit import T, add_meta, PORT


class Game:
    def __init__(self, client):
        self.black_player = Player(1, 'black', [])
        self.white_player = Player(2, 'white', [self.black_player])
        self.black_player.other_players = [self.white_player]

        self.board = None
        self.continue_ = False
        self.hand_figure = None
        self.board_locked = False

        self.client = client
        self.client.start_loop(self.loop)

        self.screen = None

    def loop(self):
        msg = self.client.recv()
        if T.MOVE(msg):
            self.board_locked = False

    def set_board(self, board):
        self.board = board

    def other_player(self, player):
        if player is self.black_player:
            return self.white_player
        return self.black_player

    def run(self):
        if self.board is None:
            print('Can\'t start game, game.board is None')
            return
        if self.screen is None:
            print("Can't start game, game.screen is None")
        self.continue_ = True

    def set_screen(self, screen):
        self.screen = screen

    def stop(self):
        self.continue_ = False

    @property
    def continue_game(self):
        return self.continue_

    def figure_eaten(self, figure):
        pass

    def record_move(self, from_, to):
        self.board_locked = True
        self.client.send(add_meta({
            'from': (from_.col, from_.row),
            'to': (to.col, to.row),
        }, T.MOVE))
        print(f'MOVE: {from_} -> {to}')


game = Game(SocketClient('127.0.0.1', PORT))
