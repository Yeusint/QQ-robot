from ping import Ping
from json import loads
from threading import Thread
from time import sleep
node = loads(open("res/data.json", "r").read())['node']


def thead(args: int):
    a = Ping(node[args], 80, 50)
    a.ping(4)
    print(a.result.rows[0][7])


i = 0
while i < len(node):
    Thread(target=thead, args=(i,)).start()
    i += 1
