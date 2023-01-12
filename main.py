import time

import pygame

from constants import WIDTH, HEIGHT, BG
from board import Board
from game import game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game.set_screen(screen)

board = Board(screen, 1, 1, square_cells=True)
board.use_default_config(1)
game.set_board(board)

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
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    sel_cell = board.cell(*board.selected_cell)
                    if sel_cell.figure.can_move_to(clicked_cell):
                        sel_cell.figure.move_to(clicked_cell)
                    board.selected_cell = None
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif evt.type == pygame.MOUSEMOTION:
            curr_cell = board.cell_by_coords(evt.pos)
            if board.selected_cell is not None:
                sel_cell = board.cell(*board.selected_cell)
                if board.selected_cell is not None and curr_cell is not None and sel_cell.figure.can_move_to(curr_cell) or sel_cell is curr_cell:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                if curr_cell is None or curr_cell.figure is None:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


    screen.fill(BG)
    board.draw()

    pygame.display.flip()

    time.sleep(0.01)