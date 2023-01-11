import time

import pygame

from constants import WIDTH, HEIGHT, BG
from board import Board
from figures.bishop import Bishop
from figures.pawn import Pawn
from figures.rook import Rook
from game import game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game.set_screen(screen)

board = Board(screen, 8, 8, square_cells=True)
game.set_board(board)
for i in range(8):
    board.cell(i, 6).figure = Pawn(board.cell(i, 6), game.white_player)
    board.cell(i, 1).figure = Pawn(board.cell(i, 1), game.black_player)
board.cell(5, 5).figure = Rook(board.cell(5, 5), game.black_player)
game.run()

while game.continue_game:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            game.stop()
        elif evt.type == pygame.WINDOWRESIZED:
            board.screen_resized()
        elif evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == pygame.BUTTON_LEFT:
                clicked_cell = board.cell_by_coords(evt.pos)
                if board.selected_cell is None or clicked_cell is None:
                    if clicked_cell is None or clicked_cell.figure is None:
                        board.selected_cell = None
                    else:
                        board.selected_cell = clicked_cell.col, clicked_cell.row
                else:
                    sel_cell = board.cell(*board.selected_cell)
                    if sel_cell.figure.can_move_to(clicked_cell):
                        sel_cell.figure.move_to(clicked_cell)
                    board.selected_cell = None

    screen.fill(BG)
    board.draw()

    pygame.display.flip()

    time.sleep(0.01)