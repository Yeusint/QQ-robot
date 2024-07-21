from socket import socket, AF_INET, SOCK_DGRAM

c = socket(AF_INET, SOCK_DGRAM)
addr = ('127.0.0.1', 8888)
mq = 0
mq_cache = {}

def hex_int(h):
    return int.from_bytes(bytes.fromhex("0"*(len(h)%2)+h), 'big')

def get_data():
    if mq in mq_cache:
        m = mq_cache.pop(mq)
    else:
        m = c.recvfrom(1024)[0]
    sn = hex_int(m.decode().split('|')[0])
    while sn != mq:
        mq_cache[sn] = m
        c.sendto(f'{sn}|Back'.encode(), addr)
        c.recvfrom(1024)
    c.sendto(f'{sn}|Back'.encode(), addr)
    return True

name = input('输入你的名字->')
msg = c.recvfrom(1024)[0].decode()
if msg.startswith('Failed'):
    print('名字被占用!')
    exit(114514)
uid = msg[msg.find('|')+1:]

if input('连接还是等待连接[1]/2->') != 2:
    tar = input('输入对方id->')
    '' if tar.isdigit() else exit(114514)
    mq+=1
    c.sendto(f'{mq}|check|{uid}|{tar}', addr)
    msg = get_data()
    while True:
        if check_data(msg):
            break
    msg = msg
