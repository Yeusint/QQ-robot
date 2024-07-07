from lib import SUDP

s = SUDP('127.0.0.1', 8888)

@s.cmd()
def log(msg, addr):
    print(f'来自{addr}的消息{msg}')

@s.cmd('abc')
def abc(msg, addr):
    print(msg, addr)

s.start()
