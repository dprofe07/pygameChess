from client.player import Player
from client.socket_client import SocketClient
from socket_toolkit import T, add_meta, PORT


class Game:
    def __init__(self, player):
        self.black_player = Player(1, 'black', [])
        self.white_player = Player(2, 'white', [self.black_player])
        self.black_player.other_players = [self.white_player]

        self.current_player = self.white_player if player == 'white' else self.black_player

        self.board = None
        self.continue_ = False
        self.hand_figure = None
        self.board_locked = False
        self.reversed_board = self.current_player is self.black_player

        self.client = SocketClient('127.0.0.1', PORT)
        lst = [int(i.replace('CHESS_', '')) for i in self.client.get_room_list()['rooms']]
        if len(lst) == 0:
            lst = [1]
        n = lst[-1] + 1
        if self.current_player is self.white_player:
            self.client.send({
                'name': f'CHESS_{n}'
            }, T.CREATE_ROOM)
            data = self.client.recv()
            if T.REJECT(data):
                raise Exception('Troubles')
            self.client.send({
                'name': f'CHESS_{n}'
            }, T.JOIN_ROOM)
        else:
            self.client.send({
                f'name': f'CHESS_{n - 1}'
            }, T.JOIN_ROOM)
            self.board_locked = True
        self.client.start_loop(self.loop)
        self.screen = None

    def loop(self):
        msg = self.client.recv()
        if T.MOVE(msg):
            from_ = msg['from']
            to = msg['to']
            cell_from = self.board.cell(*from_)
            cell_to = self.board.cell(*to)
            if cell_from.figure is None:
                print(f'Troubles with cell {cell_from}')
                return
            if cell_to is None:
                print(f'Troubles with cell {cell_to}')
                return
            cell_from.figure.move_to(cell_to)
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
        self.client.close()
        self.continue_ = False

    @property
    def continue_game(self):
        return self.continue_

    def figure_eaten(self, figure):
        pass

    def record_move(self, from_, to):
        self.board_locked = True
        self.client.send({
            'from': (self.board.width - 1 - from_.col, self.board.width - 1 - from_.row),
            'to': (self.board.height - 1 - to.col, self.board.height - 1 - to.row),
        }, T.MOVE)
        print(f'MOVE: {from_} -> {to}')


# game = Game('whit')
