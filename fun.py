import socket
import hashlib
import requests
from json import loads
from random import randint
from datetime import date


def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))
    payload = ''
    msg_type = resp_dict['type']  # 回复类型（群聊/私聊）
    number = resp_dict['id']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def send_request(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))
    if resp_dict['type'] == 'group' and 'reason' in resp_dict:
        payload = "GET /set_group_add_request?flag=" + str(resp_dict['flag']) + \
                  "&sub_type=" + resp_dict['sub_type'] + \
                  '&approve=' + resp_dict['approve'] + \
                  "&reason=" + resp_dict['reason'] + \
                  " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif resp_dict['type'] == "group" and 'reason' not in resp_dict:
        payload = "GET /set_group_add_request?flag=" + str(resp_dict['flag']) + \
                  "&sub_type=" + resp_dict['sub_type'] + \
                  '&approve=' + resp_dict['approve'] + \
                  " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif resp_dict['type'] == 'friend':
        payload = "GET /set_friend_add_request?flag=" + str(resp_dict['flag']) + \
                  "&sub_type=" + resp_dict['sub_type'] + \
                  '&approve=' + resp_dict['approve'] + \
                  " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    else:
        send_msg({
            'type': 'private',
            'id': '673457979',
            'msg': '主人！报告机器人代码执行错误！'
        })
        return 0
    print("处理请求" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def quit_group(id_):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))
    payload = "GET /set_group_leave?group_id=" + str(id_) + \
              " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("退群" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def get_group_list():
    html = requests.get("http://127.0.0.1:5700/get_group_list")
    json_text = str(loads(html.text)['data'])
    i = 2
    data = ''
    result = ''
    while i < len(json_text) - 2:
        data = data + json_text[i]
        i += 1
    data = data.split("}, {")
    i = 0
    while i < len(data):
        data[i] = '{' + data[i] + '}'
        result = result + data[i][data[i].index('group_name') + 14:data[i].index('\', \'max_member_count')] + "\n"
        i += 1
    return result + "-----------------------"


def set_group_admin(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))
    group_id = resp_dict['group']
    number = resp_dict['id']
    set_type = resp_dict['set']
    payload = "GET /set_group_admin?group_id=" + str(group_id) + \
              "&user_id=" + number + \
              '&enable=' + str(set_type) + \
              " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("管理员操作" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def get_md5(str_):
    parm_str = ''
    if isinstance(str_, str):
        parm_str = str_.encode("utf-8")
    m = hashlib.md5()
    m.update(parm_str)
    return m.hexdigest()


def translate(text, language):
    if language not in open("config.txt", 'r').read().split(','):
        return None
    else:
        from_ = 'auto'
        to = language
        app_id = '20220312001121848'
        key = '3ub5oSCnDyVJWDteblZW'
        salt = str(randint(200000, 900000))
        url = "https://api.fanyi.baidu.com/api/trans/vip/translate?q=" + text + \
              "&from=" + from_ + \
              "&to=" + to + \
              "&appid=" + app_id + \
              "&salt=" + salt + \
              "&sign=" + str(get_md5(app_id + text + salt + key))
        html = requests.get(url)
        json_text = str(dict(loads(html.text))['trans_result'])
        result = json_text[json_text.index("dst") + 7:-3]
        return result


def get_music(t, type_='search', other=''):
    _hash = ['', '', '', '', '', '', '', '', '', '']
    if type_ == 'search' or type_ == 'dash':
        html = requests.get(
            'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=' + t + '&page=1&pagesize=20&showtype=1'
        )
        music_search = loads(html.text)
        i = 0
        name = ''
        while i < 10:
            _hash[i] = music_search['data']['info'][i]['hash']
            name = name + str(i + 1) + ' ' + music_search['data']['info'][i]['filename'] + '\n'
            i += 1
        if type_ == 'search':
            return name
        else:
            return _hash
    elif type_ == 'get':
        html = requests.get("http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=" + t)
        music_search = loads(html.text)
        if t != '':
            result = music_search['url']
            return result
        else:
            return None
    elif type_ == 'other':
        if t != '' and other != '':
            data = loads(requests.get("http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=" + t).text)
            return data[other]
        else:
            return None
    else:
        return None


def get_weather(type_, place):
    txt = open("tidy.txt", 'r', encoding='UTF-8').read()
    tidy_name = txt[0:txt.find('_')].splitlines()
    tidy_code = txt[txt.find('_') + 2:len(txt)].splitlines()
    headers = {
        'Accept': 'text/html,'
                  'application/xhtml+xml,'
                  'application/xml;q=0.9,'
                  'image/avif,'
                  'image/webp,'
                  'image/apng,'
                  '*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_187fda34c81598ec29ebc4da675267cc=1647742632;'
                  ' ASPSESSIONIDQUQRTCAB=CBILGFEDILOKGAGDKOMNDGLI;'
                  ' ASPSESSIONIDSUSQRADB=JNHPGFEDLGLFJILJFDJIENJD;'
                  ' ASPSESSIONIDSWSSTDCA=BPHJGFEDECALNBDMFKNJLHCE;'
                  ' ASPSESSIONIDQUSTQBBB=BFHHFFEDBNFCGMNDHKKHNAMF;'
                  ' ASPSESSIONIDQURQTDAA=DLHNFFEDNNDFKMPHKFHJIJAC;'
                  ' ASPSESSIONIDSWSTTAAA=BCIJFFEDBAFCLMIFNJJDGALK;'
                  ' ASPSESSIONIDQWQRSADB=NNHDGFEDJNHPKIKBOHPKBEJJ;'
                  ' ASPSESSIONIDQWSQTAAA=MFIBFFEDOBHNEJGGLCEGNBCC;'
                  ' ASPSESSIONIDQURSRBAD=HIILFFEDAJOMGKIIEGHIDOOM;'
                  ' ASPSESSIONIDQWSTQAAB=KGBENIEDLIFHLGCGIOLJKBLM;'
                  ' ASPSESSIONIDSUSTRCAA=AINBFFEDPIGLHDHNDBNBNBLE;'
                  ' ASPSESSIONIDSWTSTCAB=FBLJFFEDJPFKMFIAPGEFNKKB;'
                  ' ASPSESSIONIDSURTTCBA=FNAEGFEDKHBPIPELDEDAIKKC;'
                  ' ASPSESSIONIDCUQSSCDD=BMBGFFEDFHKGIHFHHECJMHAF;'
                  ' Hm_lpvt_187fda34c81598ec29ebc4da675267cc=1647751523',
        'Host': 'api.help.bj.cn',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/86.0.4240.198 Safari/537.36'
    }
    try:
        if type_ == 'today':
            data = loads(requests.request(
                'get', 'https://api.help.bj.cn/apis/weather/?id=' + tidy_code[tidy_name.index(place)], headers=headers
            ).text)
            result = "日期：" + data['today'] + "\n更新时间：" + data['uptime'] \
                     + "\n------------------------\n地区：" + data['city'] \
                     + "\n气温：" + data['weather'] + data['temp'] + "°C" \
                     + "\n风向风力：" + data['wd'] + data['wdforce']
            return result
        elif type_ == "will":
            data = loads(requests.request(
                'get', 'https://api.help.bj.cn/apis/weather6d/?id=' + tidy_code[tidy_name.index(place)], headers=headers
            ).text)['data']
            result = '[最近六日天气]' \
                     '\n月份：' + str(date.today().month) + '月' \
                                                         '\n城市：' + data['city'] + \
                     '\n--------------------------' \
                     '\n日期：' + data['yesterday']['date'] + \
                     '\n气温：' + data['yesterday']['templow'] + '°C-' + data['yesterday']['temphigh'] + '°C' \
                                                                                                      '\n风力：' + \
                     data['yesterday']['wind'] + data['yesterday']['windforce'] + \
                     '\n--------------------------'
            i = 0
            while i < len((data['forecast'])):
                result = result + \
                         '\n日期：' + data['forecast'][i]['date'] + \
                         '\n气温：' + data['forecast'][i]['templow'] + '°C-' + data['forecast'][i]['temphigh'] + '°C' \
                                                                                                              '\n风力：' + \
                         data['forecast'][i]['wind'] + data['forecast'][i]['windforce'] + \
                         '\n--------------------------'
                i += 1
            return result + "\n温馨提示：" + data['life']
        else:
            return None
    except ValueError:
        return None


def download(url, file):
    url = requests.get(url)
    open(file, 'wb').write(url.content)
