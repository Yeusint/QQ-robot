import time

from fun import *
from receive import *

# ---------------------------
fdj = False
music = False
music_card = False
hash_ = ['', '', '', '', '', '', '', '', '', '']
while True:
    text = rev_msg()
    if 'interval' not in text:
        print(text)
    else:
        pass
    if 'message' in text:
        if text['message_type'] == "group":
            if '有人吗' in text['message']:
                send_msg({
                    'type': 'group',
                    'id': text['group_id'],
                    'msg': '[CQ:at,qq=' + str(text['user_id']) + ']我在，想干啥[CQ:face,id=178]'})
            if text['message'] == '开启复读机':
                if text['user_id'] == 673457979:
                    send_msg({
                        'type': 'group',
                        'id': str(text['group_id']),
                        'msg': '[CQ:at,qq=673457979]遵命，主人！已开启复读机~[CQ:face,id=179]被管理员误禁言请帮我解了哦~[CQ:face,id=20]'
                    })
                    fdj = True
                else:
                    send_msg({
                        'type': 'group',
                        'id': str(text['group_id']),
                        'msg': '[CQ:tts,text=你不是我家主人，我只听我家主人的哦~]'
                    })
            elif text['message'] == '关闭复读机':
                fdj = False
                send_msg({
                    'type': 'group',
                    'id': str(text['group_id']),
                    'msg': '[CQ:at,qq=673457979]好的，主人！已关闭复读机啦~[CQ:face,id=179]'
                })
            elif text['message'] == '翻译':
                send_msg({
                    'type': 'group',
                    'id': text['group_id'],
                    'msg': "[翻译]\n"
                           "---------------------------\n"
                           "翻译+目标语种代码[空格]需要翻译的文本\n"
                           "---------------------------\n"
                           "例：翻译zh apple\n"
                           "语种代码参考↓\n"
                           "[CQ:image,file=file:///D:/bf/code/python-code/qq-robot2/language.png,id=40000]"
                })
            elif text['message'] == "点歌":
                send_msg({
                    'type': 'group',
                    'id': text['group_id'],
                    'msg': "[点歌]\n"
                           "---------------------------\n"
                           "点歌+歌名\n"
                           "---------------------------\n"
                           "例：点歌小苹果\n"
                           "当前仅支持酷狗渠道，其它渠道正在开发中..."
                })
            elif text['message'] == '查询天气':
                send_msg({
                    'type': 'group',
                    'id': text['group_id'],
                    'msg': '[查询天气]'
                           "\n---------------------------"
                           "\n今日天气[地名]"
                           "\n最近六日天气[地名]"
                           "\n---------------------------"
                           "\n仅供参考，此API连作者都觉得不靠谱[CQ:face,id=178]"
                })
            elif text['message'] == '切换音乐形式':
                if music_card is False:
                    music_card = True
                    send_msg({
                        'type': 'group',
                        'id': text['group_id'],
                        'msg': '[音乐形式]'
                               '\n---------------------------'
                               '\n音乐播放形式切换成功~[CQ:face,id=101]'
                               '\n当前音乐播放形式:卡片'
                    })
                else:
                    music_card = False
                    send_msg({
                        'type': 'group',
                        'id': text['group_id'],
                        'msg': '[音乐形式]'
                               '\n---------------------------'
                               '\n音乐播放形式切换成功~[CQ:face,id=101]'
                               '\n当前音乐播放形式:语音'
                    })
            elif ' ' in text['message'] and len(text['message']) > 5 and text['message'][0:2] == "翻译":
                i = 2
                g = ''
                while i < text['message'].index(' '):
                    g = g + text['message'][i]
                    i += 1
                g_1 = text['message'][text['message'].index(' ')+1:len(text['message'])]
                result = translate(g_1, g)
                if result is None:
                    send_msg({
                        'type': 'group',
                        "id": text['group_id'],
                        'msg': "[CQ:at,qq=" + str(text["user_id"]) + "]请正确填写语种！"
                    })
                else:
                    send_msg({
                        'type': 'group',
                        "id": text['group_id'],
                        'msg': "原文：" + g_1 + "\n译文：" + result
                    })
            elif len(text['message']) > 0 and text['message'][0] == "说":
                i = 1
                t = ''
                while i < len(text['message']):
                    t = t + text['message'][i]
                    i += 1
                mp = 'https://tts.baidu.com/text2audio?tex=' + t +\
                     '&cuid=baike&lan=ZH&ctp=5&pdt=301&vol=5&rate=32&per=0'
                download(mp, 'r.mp3')
                send_msg({
                    'type': 'group',
                    "id": text['group_id'],
                    'msg': "[CQ:record,file=file:///D:/bf/code/python-code/qq-robot2/r.mp3]"
                })
            elif len(text['message']) > 2 and text['message'][0:2] == "点歌":
                i = 2
                t = ''
                while i < len(text['message']):
                    t = t + text['message'][i]
                    i += 1
                music = True
                send_msg({
                    'type': 'group',
                    'id': text['group_id'],
                    'msg': "[点歌]\n请发送序号以选择歌曲\n----------------------------------\n" + get_music(t)
                })
                hash_ = get_music(t, 'dash')
            elif len(text['message']) > 4 and text['message'][0:4] == "今日天气":
                try:
                    send_msg({
                        'type': 'group',
                        'id': text['group_id'],
                        'msg': "[今日天气]\n" + get_weather('today', text['message'][4:len(text['message'])])
                    })
                except:
                    pass
            elif len(text['message']) > 6 and text['message'][0:6] == "最近六日天气":
                result = get_weather('will', text['message'][6:len(text['message'])])
                if result is not None:
                    send_msg({
                        'type': 'group',
                        'id': text['group_id'],
                        'msg': result
                    })
                else:
                    pass
            elif fdj:
                send_msg({
                    'type': 'group',
                    'id': str(text["group_id"]),
                    'msg': str(text['message'])
                })
            elif music:
                if text['message'].isdigit() is True and int(text['message']) < 10:
                    f = get_music(hash_[int(text['message']) - 1], 'get')
                    if f == '':
                        send_msg({
                            'type': 'group',
                            'id': text['group_id'],
                            'msg': "此音乐需要付费，无法播放-_-"
                        })
                    elif f is None:
                        send_msg({
                            'type': 'group',
                            'id': text['group_id'],
                            'msg': "API错误，请联系作者[CQ:at,qq=673457979]进行修复-_-"
                        })
                    else:
                        if music_card is False:
                            send_msg({
                                'type': 'group',
                                'id': text['group_id'],
                                'msg': "[CQ:record,file=" + f + "]"
                            })
                        else:
                            send_msg({
                                'type': 'group',
                                'id': text['group_id'],
                                'msg': str('[CQ:music,type=custom,url=http://110.40.149.75/cs,audio=' + f + ',title=' + get_music(hash_[int(text['message']) - 1], 'other', 'fileName') + ',content=Yeusint®\n由YST Studio版权所有©,image=http://q1.qlogo.cn/g?b=qq&nk=' + text['user_id'] + '&s=0]')
                            })
                    music = False
            else:
                pass
            if text['user_id'] == 673457979:
                if len(text['message']) > 2 and text['message'][0] + text['message'][1] == "加管":
                    i = 2
                    g = ''
                    while i < len(text['message']):
                        g = g + text['message'][i]
                        i += 1
                    set_group_admin({
                        'group': text['group_id'],
                        'id': g,
                        'set': True
                    })
                    send_msg({
                        'type': 'group',
                        "id": text['group_id'],
                        'msg': "[CQ:at,qq=673457979]已成功添加[CQ:at,qq=" + g + ']为管理员！'
                    })
                elif len(text['message']) > 2 and text['message'][0] + text['message'][1] == "减管":
                    i = 2
                    g = ''
                    while i < len(text['message']):
                        g = g + text['message'][i]
                        i += 1
                    set_group_admin({
                        'group': text['group_id'],
                        'id': g,
                        'set': False
                    })
                    send_msg({
                        'type': 'group',
                        "id": text['group_id'],
                        'msg': "[CQ:at,qq=673457979]已成功将[CQ:at,qq=" + g + ']移除管理员！'
                    })
                elif len(text['message']) > 2 and text['message'][0] + text['message'][1] == '退群':
                    i = 2
                    n = len(text['message'])
                    g = ''
                    while i < n:
                        g = g + text['message'][i]
                        i += 1
                    if g.isdigit() is True:
                        send_msg({
                            'type': 'group',
                            'id': g,
                            'msg': '[CQ:tts,text=群里的各位，我将在3秒后退群，拜拜~]'
                        })
                        time.sleep(3)
                        quit_group(g)
                    else:
                        pass
                elif text['message'] == "获取群列表":
                    send_msg({
                        'type': 'group',
                        'id': text['group_id'],
                        'msg': get_group_list() + "\n已展示全部~"
                    })
    if 'flag' in text:
        send_request({
            'type': 'group',
            'flag': text['flag'],
            'sub_type': text['sub_type'],
            'approve': 'true'
        })
