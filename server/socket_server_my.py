import socket
from threading import Thread
from socket_toolkit import *
from server.socket_server import servfunc, ServerFunction, Server as StdServer, Client


class Server(StdServer):
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((address, port))
        self.serv_funcs = {
            a.command: a for k in dir(self)
            if type(a := getattr(self, k)) == servfunc
        }
        self.current_idx = 0
        self.rooms = {}
        self.clients = {}

    def

    def log(self, content, title='SERVER'):
        print(f'[{title}] {content}')

    def start(self):
        thr = Thread(target=self._accept_loop)
        thr.start()

    def disconnect(self, conn):
        try:
            h_send(conn, meta(T.DISCONNECT))
            conn.close()
        except:
            self.log(f'Failed disconnecting from {conn}')

    def close(self):
        for r in self.rooms.values():
            r.close()
        self.sock.close()


server = Server(SERVER, PORT)
server.start()



class ChatWindow:
    def __init__(self, client):
        self.client = client
        self.client.start_loop(self.loop)

    def loop(self):
        print('LOOP ITER')
        msg = self.client.recv()
        author, text = msg['author'], msg['msg']
        self.append_chat(text, author)

    def send(self):
        self.client.send({
            'author': '123',
            'msg': v
        })

    def append_chat(self, text, author):
        s = f'{author}: {text}'
        print('SHOULD BE IN CHUT', s)