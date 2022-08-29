from fun.ping import Ping
from json import loads, dumps
from threading import Thread
from time import sleep
from graia.ariadne.entry import Image
config = loads(open("res/data.json", "r").read())
node = config["node"]
speed_result = {}


def thread(args: int):
    a = Ping(node[args], 80, 50)
    a.ping(4)
    speed_result[node[args]] = a.result.rows[0][7]


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
            result += node[i] + "|" + result_list[node[i]] + "\n"
            i += 1
        return result


def get_admin_list(group_id: int):
    try:
        data = config["admin"][str(group_id)]
    except KeyError:
        config["admin"][str(group_id)] = []
        open("res/data.json", "w").write(str(config))
        return ["俺在这个群没有管理员喔~", Image(path="res/a1.png")]
    if data is []:
        return ["俺在这个群没有管理员喔~", Image(path="res/a1.png")]
    return data
