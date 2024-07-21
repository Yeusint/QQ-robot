# 点歌系统
from graia.ariadne.message.element import MusicShareKind
from graia.ariadne.entry import (
    Ariadne,
    GroupMessage,
    Group,
    MessageChain,
    Member,
    Face,
    DetectPrefix,
    At,
    MusicShare
)
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from fun.cache_var import song_cache
from fun.music import get_kugou, song_data
a = Channel.current()
b = Channel.current()


@a.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix("点歌")]))
async def a(app: Ariadne, group: Group, mem: Member, msg: MessageChain = DetectPrefix("点歌")):
    if msg.display == '':
        await app.send_message(group, MessageChain(
            "[点歌]\n----------------------\n",
            "目前使用语音方式发送,后续更新卡片方式发送喔~\n",
            '出现列表后直接发送数字即可等待收听啦~\n格式：点歌[歌名]\n------------------------\n',
            '目前普通音乐使用酷狗渠道播放,VIP歌曲使用QQ音乐渠道播放'
        ))
    else:
        data = get_kugou(msg.display)
        song_cache[mem.id] = data
        i=0
        r=''
        while i != 10:
            r+=str(i+1) + " " + data[i]["FileName"] + "\n"
            i+=1
        await app.send_message(group, MessageChain(
            At(mem),
            " 请输入序号~",
            Face(name="眨眼睛"),
            "\n",
            r
        ))


@b.use(ListenerSchema(listening_events=[GroupMessage]))
async def b(app: Ariadne, g: Group, mem: Member, msg: MessageChain):
    if mem.id in song_cache and msg.display.isdigit():
        num = int(msg.display)
        cookies = {
            'dfid': '2C7nx20YQMEs0yz5uR1RaHXI',
            'KuGoo': 'KugooID=875231868&KugooPwd=FCDD11161D9C9444E7AF9192682FB26D&NickName=%u4e00%u4e2a%u0032%u0035%u0030&Pic=http://imge.kugou.com/kugouicon/165/20100101/20100101192931478054.jpg&RegState=1&RegFrom=&t=d471095e761713ffb3eec6c5a6d5e38e7cc5a2e60878bfd942f7315ccaa07348&t_ts=1673014559&t_key=&a_id=1014&ct=1673014559&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0038%u0037%u0035%u0032%u0033%u0031%u0038%u0036%u0038',
            'UserName': '%u006b%u0067%u006f%u0070%u0065%u006e%u0038%u0037%u0035%u0032%u0033%u0031%u0038%u0036%u0038',
            't': 'd471095e761713ffb3eec6c5a6d5e38ecd60c37d67261634efe5af25a01bede2',
            'KugooID': '875231868',
            'kg_dfid_collect': 'd41d8cd98f00b204e9800998ecf8427e',
            'kg_mid': '9e2f6588ff79eb10e50a8e27e13d8dc4',
            'mid': '9e2f6588ff79eb10e50a8e27e13d8dc4',
            'kg_dfid': '2C7nx20YQMEs0yz5uR1RaHXI',
            'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d': '1672647423,1672708939,1672709956,1672793270',
            'UM_distinctid': '181e5c6e5bafb-0f2109c82915ac-9136f2c-15f900-181e5c6e5bb248'
        }
        if 10 >= num >= 1:
            data = song_cache[mem.id][num-1]
            song_cache.pop(mem.id)
            data_ = song_data(data['EMixSongID'], 'kugou', cookies)
            await app.send_message(g, MessageChain(
                '酷狗新接口,作者使用两天半研究出来的,能给作者[赞助]一下嘛',
                Face(name='眨眼睛')
            ))
            await app.send_message(g, MessageChain(MusicShare(
                MusicShareKind.KugouMusic,
                data['OriSongName'],
                data['FileName'],
                f'https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord={data["OriSongName"]}',
                data_['img'],
                data_['play_url'],
                data['OriSongName']
            )))
