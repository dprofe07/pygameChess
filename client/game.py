import pygame

from client.player import Player
from client.socket_client import SocketClient
from pyautogui import prompt, confirm

from constants import BG
from socket_toolkit import T, add_meta, PORT, SERVER, meta


class Game:
    def __init__(self, player):
        self.black_player = Player(1, 'black', [])
        self.white_player = Player(2, 'white', [self.black_player])
        self.black_player.other_players = [self.white_player]

        self.current_player = self.white_player if player == 'white' else self.black_player

        self.board = None
        self.continue_ = False
        self.hand_figure = None
        self.left_btn_pressed = False
        self.board_locked = False
        self.connected = False
        self.winner = True
        self.reversed_board = self.current_player is self.black_player

        self.client = SocketClient(SERVER, PORT)

        create_room = confirm('Подключение к шахматам', 'Подключение', ['Создать игру', 'Присоединиться к игре']) == 'Создать игру'

        room_name = prompt('Введите имя комнаты', 'Подключение', None)
        if room_name is None:
            exit(0)

        if create_room:
            self.client.send({
                'name': room_name,
            }, T.CREATE_ROOM)
            data = self.client.recv()
            if T.REJECT(data):
                raise Exception('Troubles')

        self.client.send({
            f'name': room_name,
        }, T.JOIN_ROOM)
        self.client.recv()

        if not create_room:
            self.client.send({}, T.CAN_START)
            self.connected = True

        self.board_locked = True
        self.client.start_loop(self.loop)
        self.screen = None
        self.need_redraw = True

    def loop(self):
        msg = self.client.recv()
        if T.MOVE(msg) and msg['sender'] != self.current_player.id:
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
            cell_from.figure.move_to(cell_to, False)
            self.board_locked = False
            self.need_redraw = True
        elif T.CAN_START(msg) and not self.connected:
            self.connected = True
            if self.current_player is self.black_player:
                self.client.send({}, T.CAN_START)
            else:
                self.board_locked = False

            self.need_redraw = True
        elif T.GAME_END(msg):
            self.winner = True
            self.game_end()

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

    def get_status_text(self):
        if not self.connected:
            return 'Ждём подключения оппонента'
        else:
            if self.winner:
                return "ПОБЕДА!"

            if self.board_locked:
                return 'Ход соперника'
            else:
                return 'Ваш ход'

    @property
    def continue_game(self):
        return self.continue_

    def figure_eaten(self, figure):
        pass

    def record_move(self, from_, to):
        self.board_locked = True
        self.client.send({
            'sender': self.current_player.id,
            'from': (self.board.width - 1 - from_.col, self.board.height - 1 - from_.row),
            'to': (self.board.width - 1 - to.col, self.board.height - 1 - to.row),
        }, T.MOVE)
        print(f'MOVE: {from_} -> {to}')

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()
        elif event.type == pygame.WINDOWRESIZED:
            self.board.screen_resized()
            self.need_redraw = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.board_locked:
                self.left_btn_pressed = False
                self.set_standart_cursor()
                return

            if event.button == pygame.BUTTON_LEFT:
                self.left_btn_pressed = True
                clicked_cell = self.board.cell_by_coords(event.pos)

                if self.board.selected_cell is None:
                    if (
                            clicked_cell is None or
                            clicked_cell.figure is None or
                            clicked_cell.figure.player is not self.current_player
                    ):
                        self.board.select_cell(None)
                        self.set_standart_cursor()
                    else:
                        self.board.select_cell(clicked_cell.coords())
                        self.set_pointer_cursor()
                else:
                    if self.board.selected_cell.figure.can_move_to(clicked_cell):
                        self.board.selected_cell.figure.move_to(clicked_cell)
                        self.board.select_cell(None)
                        self.set_standart_cursor()
                    else:
                        self.board.select_cell(clicked_cell.coords())
                        self.set_pointer_cursor()
                self.need_redraw = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.board_locked:
                return

            if event.button == pygame.BUTTON_LEFT:
                self.left_btn_pressed = False

                if self.hand_figure is not None:
                    pos = pygame.mouse.get_pos()
                    curr_cell = self.board.cell_by_coords(pos)

                    if curr_cell is None or not self.hand_figure.can_move_to(curr_cell):
                        self.board.selected_cell.figure = self.hand_figure
                    else:
                        self.hand_figure.move_to(curr_cell)
                    self.hand_figure = None
                    self.board.select_cell(None)
                    self.need_redraw = True

        elif event.type == pygame.MOUSEMOTION:
            if self.board_locked:
                self.set_standart_cursor()
                return
            self.need_redraw = True

            if self.left_btn_pressed:
                if self.board.selected_cell is not None and self.hand_figure is None:
                    if self.board.selected_cell is not None:
                        self.hand_figure = self.board.selected_cell.figure
                        self.board.selected_cell.figure = None
            else:
                curr_cell = self.board.cell_by_coords(event.pos)
                if self.board.selected_cell is not None:
                    if curr_cell is not None and self.board.selected_cell.figure.can_move_to(curr_cell) or self.board.selected_cell is curr_cell:
                        self.set_pointer_cursor()
                    else:
                        self.set_standart_cursor()
                else:
                    if curr_cell is None or curr_cell.figure is None:
                        self.set_standart_cursor()
                    else:
                        self.set_pointer_cursor()

    @staticmethod
    def set_pointer_cursor():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    @staticmethod
    def set_standart_cursor():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self):
        if not self.need_redraw:
            return

        self.screen.fill(BG)
        self.board.draw(pygame.mouse.get_pos(), self.get_status_text())
        if self.hand_figure is not None:
            pos = pygame.mouse.get_pos()
            fig = self.hand_figure.image
            rect = fig.get_rect(center=pos)
            self.screen.blit(fig, rect)
        pygame.display.flip()

        self.need_redraw = False

    def game_end(self):
        if not self.winner:
            self.client.send({}, T.GAME_END)


# game = Game('white')
