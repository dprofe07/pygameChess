from server.game import Game
from server.socket_server import Server

class ChessServer:
    def __init__(self):
        self.games = []
        self.sock = Server('0.0.0.0', 9812)
        self.sock.start()


    def game_created(self, user1, user2):
        id_ = len(self.games)
        self.games.append(Game(user1, user2, id_))

    def wait_for_game(self):
        user1 = self.sock.
