import socket
from threading import Thread
from socket_toolkit import *


class servfunc:
    def __init__(self, command):
        self.command = command
    
    def past_init(self, func):
        self.func = func
        return self

    def __call__(self, *args):
        return self.func(*args)


def ServerFunction(command):
    sf = servfunc(str(command))
    return sf.past_init


class Client:
    def __init__(self, idx, recver):
        self.idx = idx
        self.room_name = None
        self.recver = recver

    def set_sender(self, sender):
        self.sender = sender

    def set_room(self, room_name):
        self.room_name = room_name

    def close(self):
        self.recver.close()
        self.sender.close()


class Room:
    def __init__(self, name, server):
        self.name = name
        self.server = server
        self.clients = {}

    def people_count(self):
        return len(self.clients)

    def max_capacity(self):
        return 100
    
    def add_client(self, client):
        if len(self.clients) >= self.max_capacity():
            return False
        self.clients[client.idx] = client
        return True

    def get_all_addr(self):
        return list(self.clients.keys())

    def broadcast(self, data, exclude=()):
        for client in self.clients.values():
            if client.idx in exclude:
                print('EXCLUDING!')
                continue
            try:
                print('SENDING!')
                h_send(client.recver, data)
            except Exception as ex:
                print(f'There is an error in room {self.name}: {ex}')
                self.clear()
    
    def close(self):
        for client in self.clients.values():
            self.server.disconnect(client)
        self.clients = {}
    
    def handle(self, client, data):
        if client.idx not in self.clients:
            return False
        self.broadcast(data, [client.idx])
        return True


class Server:
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

    @ServerFunction(T.GET_ROOM_LIST)
    def _get_room_list(self, msg):
        room_names = list(self.rooms.keys())
        people = [r.people_count() for r in self.rooms.values()]
        max_capacity = [r.max_capacity() for r in self.rooms.values()]
        return {
            'rooms': room_names,
            'max_capacity': max_capacity,
            'current_size': people
        }

    @ServerFunction(T.CREATE_ROOM)
    def _create_room(self, msg):
        name = msg['name']
        if name in self.rooms:
            return meta(T.REJECT)
        self.rooms[name] = Room(name, self)
        return meta(T.SUCCESS)

    @ServerFunction(T.JOIN_ROOM)
    def _join_room(self, msg):
        client = msg[UDATA_FIELD]
        room_name = msg['name']
        if room_name not in self.rooms:
            return meta(T.REJECT)
        cb = self.rooms[room_name].add_client(client)
        if cb: client.set_room(room_name)
        return meta(T.REJECT if not cb else T.SUCCESS)

    def _start_serv_func(self, tag, data):
        tag = str(tag)
        if tag not in self.serv_funcs:
            return None
        func = self.serv_funcs[tag]
        return func(self, data)

    def _check_for_meta(self, client, msg):
        data = msg.copy()
        data[UDATA_FIELD] = client
        if META_FIELD not in data:
            return False
        success = 0
        for meta_tag in data[META_FIELD]:
            cb = self._start_serv_func(meta_tag, data)
            if cb is None:
                continue
            h_send(client.recver, cb)
            success += 1
        return success > 0

    def _destroy_room(self, name):
        if name in self.rooms:
            del self.rooms[name]

    def next_idx(self):
        self.current_idx += 1
        return self.current_idx

    def _handle_socket(self, conn):
        data = h_recv(conn)
        
        if data['status'] == 'recver':
            idx = self.next_idx()
            self.clients[idx] = Client(idx, conn)
            h_send(conn, {
                'idx': idx
            })
            return
        
        idx = data['idx']
        client = self.clients[idx]
        client.set_sender(conn)

        while True:
            msg = h_recv(conn)
            if T.DISCONNECT(msg):
                client.close()
                cl_room = self.rooms[client.room_name]
                if cl_room.people_count() == 1:
                    self._destroy_room(client.room_name)
                return
            callback = self._check_for_meta(client, msg)
            if callback or client.room_name is None:
                continue
            room = self.rooms[client.room_name]
            room.handle(client, msg)

    def _accept_loop(self):
        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()
            thread = Thread(target=self._handle_socket, args=(conn,))
            thread.start()

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


server = Server('0.0.0.0', PORT) # SERVER, PORT)
server.start()