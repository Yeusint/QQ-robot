import socket
import json

from requests import post

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)
HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html
'''


def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    client.connect((ip, 5700))
    msg_type = resp_dict['type']  # 回复类型（群聊/私聊）
    number = resp_dict['QQ']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")
    payload = ''
    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'people':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def delete_msg(id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    client.connect((ip, 5700))
    payload = "GET /delete_msg?message_id=" + str(
        id) + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def get_group_name(id):
    response = post('http://110.40.149.75:5700/get_group_member_list?group_id=' + str(id)).json()
    for i in response['data']:
        if (i['card'] != ''):
            print(i['card'] + str(i['user_id']))
        else:
            print(i['nickname'] + str(i['user_id']))


def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i] == "{" and msg[-1] == "\n":
            return json.loads(msg[i:])
    return None


# 需要循环执行，返回值为json格式
def rev_msg():  # json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    rev_json = request_to_json(Request)
    Client.sendall(HttpResponseHeader.encode(encoding='utf-8'))
    Client.close()
    return rev_json


def login(group,zh,mm):
    if zh != 'YeusintEH' or mm != 'EH-TCP':
        if zh != 'YeusintEH':
            send_msg({'type':'group','QQ':group,'msg':'账号不正确！'})
        else:
            send_msg({'type': 'group', 'QQ': group, 'msg': '密码错误！'})
    else:
        send_msg({'type': 'group', 'QQ': group, 'msg': '已登录！'})


def str_(type, text,self):
    if type == 'left':
        i = 0
        text_left_len = text.index(self)
        text_left = ''
        while i < text_left_len:
            text_left = text_left + text[i]
            i += 1
        return text_left
    elif type == 'right':
        i = text.index(self) + 1
        text_len = len(text)
        text_right = ''
        while i < text_len:
            text_right = text_right + text[i]
            i += 1
        return text_right
