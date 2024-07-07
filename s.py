from lib import SUDP
from random import randint

s = SUDP('127.0.0.1', 8888)

@s.cmd_global
def log(msg, addr):
    print(f'来自{addr[0]}:{addr[1]}的消息{msg[:20]}')

@s.cmd('check')
def abc(msg, addr, sn):
    msg:list = msg.decode().spilt('|')
    if msg[0] == 'name':
        for i in s.u_l.values():
            if msg[1] == i['name']:
                s.sock.sendto(b'Failed', addr)
                return
        while True:
            if _:= randint(1, 50) not in s.u_l:
                break
        s.sock.sendto(f'Success|{_}'.encode(), addr)
        s.u_l[_] = {'name': msg[1], 'addr': addr}
    elif msg[0] == 'uid':
        s.send(msg[1], sn, b'Success') if msg[2] in s.u_l else s.send(msg[1], sn, b'Failed')

s.start()
