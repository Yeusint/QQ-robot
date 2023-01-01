from requests import get
from graia.ariadne.entry import (
    Ariadne,
    GroupMessage,
    Group,
    MessageChain,
    Member,
    Face,
    DetectPrefix,
    Voice,
    At
)
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from json import loads
from fun.cache_var import song_cache
from graiax.silkcoder import encode
a = Channel.current()
b = Channel.current()


@a.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix("点歌")]))
async def a(app: Ariadne, group: Group, mem: Member, msg: MessageChain = DetectPrefix("点歌")):
    if msg.display == '':
        await app.send_message(group, MessageChain("🐔你太美~", Voice(path="res/j.amr")))
    else:
        data = loads(get("http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword="+msg+"&page=1&pagesize=20&showtype=1"
                         ).text)["data"]["info"]
        i=0
        r=''
        while i != 10:
            r+=str(i+1) + " " + data[i]["singername"] + '-' + data[i]["songname"] + "\n"
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
    if msg.display.isdigit():
        num = int(msg.display)
        if 10 >= num >= 1 and mem.id in song_cache:
            await app.send_message(g, MessageChain(Voice(data_bytes=encode(
                get(
                    loads(get("https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash="+song_cache[mem.id][num-1]["hash"]
                    ).text)['url']
                ).content
            ))))
