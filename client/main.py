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
        if evt.type == pygame.QUIT:
            game.stop()
        elif evt.type == pygame.WINDOWRESIZED:
            board.screen_resized()
        elif evt.type == pygame.MOUSEBUTTONDOWN:
            if not game.board_locked:
                if evt.button == pygame.BUTTON_LEFT:
                    clicked_cell = board.cell_by_coords(evt.pos)
                    if board.selected_cell is None or clicked_cell is None:
                        if clicked_cell is None or clicked_cell.figure is None or clicked_cell.figure.player is not game.current_player:
                            board.selected_cell = None
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            board.selected_cell = clicked_cell.col, clicked_cell.row
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        sel_cell = board.cell(*board.selected_cell)
                        if sel_cell.figure.can_move_to(clicked_cell):
                            sel_cell.figure.move_to(clicked_cell)
                        board.selected_cell = None
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    btn_pressed = True

        elif evt.type == pygame.MOUSEBUTTONUP:
            if not game.board_locked:
                if evt.button == pygame.BUTTON_LEFT:
                    btn_pressed = False
                    if game.hand_figure is not None:
                        pos = pygame.mouse.get_pos()
                        curr_cell = board.cell_by_coords(pos)

                        if curr_cell is None or not game.hand_figure.can_move_to(curr_cell):
                            sel_cell = board.cell(*board.selected_cell)
                            sel_cell.figure = game.hand_figure
                        else:
                            game.hand_figure.move_to(curr_cell)
                        game.hand_figure = None
                        board.selected_cell = None

        elif evt.type == pygame.MOUSEMOTION:
            if not game.board_locked:
                if btn_pressed:
                    if board.selected_cell is not None and game.hand_figure is None:
                        sel_cell = board.cell(*board.selected_cell)
                        if sel_cell is not None:
                            game.hand_figure = sel_cell.figure
                            sel_cell.figure = None
                else:
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
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    screen.fill(BG)
    board.draw(pygame.mouse.get_pos())
    if game.hand_figure is not None:
        pos = pygame.mouse.get_pos()
        fig = game.hand_figure.image
        rect = fig.get_rect(center=pos)
        screen.blit(fig, rect)
    pygame.display.flip()

    time.sleep(0.01)