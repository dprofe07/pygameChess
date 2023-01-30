import time

import pygame

from constants import WIDTH, HEIGHT, BG
from board import Board
from client.game import game
from time import perf_counter

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game.set_screen(screen)

board = Board(game, screen, 1, 1, square_cells=True)
board.load_config('std')
game.set_board(board)

game.run()

btn_pressed = False

while game.continue_game:
    for evt in pygame.event.get():
        game.handle_event(evt)
    
    game.draw()
    time.sleep(0.05)

game.game_end()