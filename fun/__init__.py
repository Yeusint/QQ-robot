from fun.ping import Ping
from json import loads
from threading import Thread
from time import sleep
node = loads(open("res/data.json", "r").read())['node']
speed_result = []


def thread(args: int):
    a = Ping(node[args], 80, 50)
    a.ping(4)
    speed_result.append(a.result.rows[0][7])


def get_speed():
    speed_result.clear()
    i = 0
    while i < len(node):
        x = Thread(target=thread, args=(i,))
        x.start()
        i += 1
    sleep(2.6)
    return speed_result


def get_speed_result(result_list: list):
    if len(node) == len(result_list):
        i = 0
        result = "共设置" + str(len(node)) + "个节点\n"
        while i < len(node):
            result += node[i] + "|" + result_list[i] + "\n"
            i += 1
        return result
