from fun.ping import Ping
from json import loads, dumps
from threading import Thread
from time import sleep
from graia.ariadne.entry import Image


speed_result = {}


def thread(args: int, node: list):
    a = Ping(node[args], 80, 50)
    a.ping(4)
    speed_result[node[args]] = a.result.rows[0][7]


def get_speed():
    config = loads(open("res/data.json", "r").read())
    node = config["node"]
    speed_result.clear()
    i = 0
    while i < len(node):
        x = Thread(target=thread, args=(i, node))
        x.start()
        i += 1
    sleep(2.6)
    return speed_result


def get_speed_result(result_list: list):
    config = loads(open("res/data.json", "r").read())
    node = config["node"]
    if len(node) == len(result_list):
        i = 0
        result = "共设置" + str(len(node)) + "个节点\n"
        while i < len(node):
            result += node[i] + "|" + result_list[node[i]] + "\n"
            i += 1
        return result


def get_admin_list(group_id: int, member_list: list) -> list:
    config = loads(open("res/data.json", "r").read())
    try:
        data = config["admin"][str(group_id)]
    except KeyError:
        config["admin"][str(group_id)] = []
        open("res/data.json", "w").write(dumps(str(config)))
        return ["俺在这个群没有管理员喔~", Image(path="res/a1.png"), 0]
    if not data:
        return ["俺在这个群没有管理员喔~", Image(path="res/a1.png"), 0]
    i = 0
    cache = {}
    while i < len(member_list):
        cache[member_list[i].id] = member_list[i].name
        i += 1
    i = 0
    result = []
    while i < len(data):
        result.append(cache[data[i]]+"(")
        result.append(str(data[i]) + ")\n")
        i += 1
    result.append(1)
    return result


def add_admin(group_id: int, member_id: int) -> list:
    config = loads(open("res/data.json", "r").read())
    try:
        config["admin"][str(group_id)].append(member_id)
        open("res/data.json", "w").write(dumps(str(config)))
        return config["admin"][str(group_id)]
    except KeyError:
        config["admin"][str(group_id)] = [member_id]
        open("res/data.json", "w").write(dumps(str(config)))
        return config["admin"][str(group_id)]


def del_admin(group_id: int, member_id: int) -> list:
    config = loads(open("res/data.json", "r").read())
    try:
        config["admin"][str(group_id)].remove(member_id)
        open("res/data.json", "w").write(dumps(str(config)))
        return config["admin"][str(group_id)]
    except KeyError:
        config["admin"][str(group_id)] = []
        open("res/data.json", "w").write(dumps(str(config)))
        return ["俺在这个群没有管理员喔~", Image(path="res/a1.png"), 0]

