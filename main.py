import time

import pygame

from constants import WIDTH, HEIGHT, BG
from board import Board

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

game_continue = True
board = Board(screen, 12, 12, square_cells=True)

while game_continue:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            game_continue = False
        elif evt.type == pygame.WINDOWRESIZED:
            board.screen_resized()

    screen.fill(BG)
    board.draw()

    pygame.display.flip()

    time.sleep(0.01)