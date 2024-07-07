from socket import socket, AF_INET, SOCK_DGRAM

c = socket(AF_INET, SOCK_DGRAM)
addr = ('127.0.0.1', 8888)

c.sendto(b'123|abc', addr)
