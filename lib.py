from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Literal
from time import sleep

class FuckError(Exception):
    pass


class SUDP:
    def __init__(self, host: str, port: int):
        if len(_:=host.split('.')) != 4:
            raise ("Invalid host.")
        for i in _:
            if not i.isdigit():
                raise "Invalid host."
        if 1 >= port or 25565 <= port:
            raise 'Invalid port.'
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.addr = (host, port)
        # Command list
        # [0] -> Call any message
        # [1] -> Specify command calls
        self.c_l = [[], {}]
        # Message queue
        # -User id
        # --Serial number->int
        # ---data->bytes
        self.m_q = {}
        # User list
        # -id->int
        # --name->str
        # --addr->tuple(ip, port->int)
        self.u_l = {}

    def start(self):
        self.sock.bind(self.addr)
        while True:
            # message data, address
            m, a = self.sock.recvfrom(1024)
            # serial number, command, message data(processed)
            try:
                _ = m.find(b'|') + 1
                if _==0:
                    raise FuckError("Fuck!!!")
                s, c, m = int.from_bytes(m[:_-1], 'big'), m[_:(_:=_+m[_:].find(b'|'))].decode(), m[_+1:]
                if c == 'Back':
                    self.do_mq(int(m), 0, s)
                    return
                for i in self.c_l[0]:
                    Thread(target=i, args=(m, a)).start()
                if c in self.c_l[1]:
                    for i in self.c_l[1][c]:
                        Thread(target=i, args=(m, a)).start()
            except Exception as e:
                print(f'Start: {e}')

    def cmd(self, name: str=None):
        def wrapper(func):
            if name:
                self.c_l[0].append(func)
            else:
                try:
                    self.c_l[1][name].append(func)
                except KeyError:
                    self.c_l[1][name] = [func]
            def __call__(*args, **kwargs):
                print("\033[31mThis function can't call!\033[0m\n\033[34mEnter: {}\033[0m".format(func.__name__))
            return __call__
        return wrapper

    def do_mq(self, uid: int, mode: Literal[0, 1], s_n: int, data:bytes=None):
        if mode:
            if data:
                self.m_q[uid][s_n] = data
            return self.m_q[uid][s_n]
        else:
            return self.m_q[uid].pop(s_n)

    def send(self, uid: int, s_n: int, data: bytes, timeout:int=5):
        def wait_back(u, t, s, d):
            for i in range(5):
                sleep(t)
                if s not in self.m_q[u]:
                    return
            self.sock.sendto(d, self.u_l[uid]['addr'])
            # Directly fuck user!!!
            self.m_q.pop(u)
            self.u_l.pop(u)
        try:
            self.sock.sendto(data, self.u_l[uid]['addr'])
            self.m_q[uid][s_n] = data
            Thread(target=wait_back, args=(uid, timeout, s_n)).start()
        except Exception as e:
            print(f'Send: {e}')

    def stop(self):
        self.sock.close()

    def __int__(self):
        _ = 0
        for i in self.m_q.values():
            _ += len(i)
        return _

    def __str__(self):
        return '!!!Watch out your mother!!!'
