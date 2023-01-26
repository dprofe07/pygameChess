import time

import pygame

from constants import WIDTH, HEIGHT, BG
from board import Board
from client.game import game

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

    screen.fill(BG)
    board.draw(pygame.mouse.get_pos())
    if game.hand_figure is not None:
        pos = pygame.mouse.get_pos()
        fig = game.hand_figure.image
        rect = fig.get_rect(center=pos)
        screen.blit(fig, rect)
    pygame.display.flip()

    time.sleep(0.01)