from requests import get
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
from json import loads
from fun.cache_var import song_cache
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
        data = loads(get("http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword="+msg+"&page=1&pagesize=20&showtype=1"
                         ).text)["data"]["info"]
        i=0
        r=''
        while i != 10:
            r+=str(i+1) + " " + data[i]["filename"] + "\n"
            i+=1
        song_cache[mem.id] = data
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
        data = song_cache[mem.id]
        song_cache.pop(mem.id)
        if 10 >= num >= 1:
            url = loads(get("https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash="+data[num-1]["hash"]
                    ).text)
            if url['url'] == "":
                m = loads(get(
                        "http://ovooa.com/API/QQ_Music/?Cookie=&msg=" +
                        data[num - 1]["singername"] +
                        "-" +
                        data[num - 1]["songname"] +
                        "&n=1&br=1"
                    ).text)['data']
                await app.send_message(g, MessageChain(MusicShare(
                    MusicShareKind.QQMusic,
                    data[num-1]["songname"],
                    "-",
                    m['url'],
                    m["picture"],
                    m["music"],
                    '此为VIP歌曲,使用QQ音乐渠道~'
                )))
            else:
                await app.send_message(g, MessageChain(MusicShare(
                    MusicShareKind.KugouMusic,
                    data[num-1]["songname"],
                    "-",
                    url['url'],
                    url["album_img"].replace("{size}", '100'),
                    url['url'],
                    '-'
                )))
