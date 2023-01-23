from board import Board
from client.game import Game as GameClient
from chess_server.player import Player


class Game(GameClient):
    def __init__(self, user1, user2, id_):
        self.user1 = user1
        self.user2 = user2
        self.id = id_

        #self.black_player = Player(1, 'black', [], '')
        #self.white_player = Player(2, 'white', [self.black_player], '')
        #self.black_player.other_players =

        self.board = Board()
        self.continue_ = False
        self.hand_figure = None
