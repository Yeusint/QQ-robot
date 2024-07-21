# 跨群消息
from graia.ariadne.exception import AccountMuted, UnknownTarget
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import Ariadne, GroupMessage, Group, MessageChain, Member, DetectPrefix, Face, At, Image
c = Channel.current()

@c.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix("跨群消息|")]))
async def a(app: Ariadne, group: Group, mem: Member, msg: MessageChain):
    data = msg.display.split("|")
    if len(data) ==3 and data[1].isdigit():
        tar = int(data[1])
        if group.id == tar:
            await app.send_message(group, MessageChain(
                "↑这位老六似乎想让我跨群跨个寂寞",
                Face(name="doge"),
                Image(path="res/a3.jpg")
            ))
            return None
        try:
            await app.send_group_message(tar, MessageChain(
                '收到跨群消息~',
                Face(name='卖萌'),
                '\n来自群:',
                group.name,
                '(',
                str(group.id),
                ')\n发送人:',
                mem.name,
                '(',
                str(mem.id),
                ')\n↓以下为消息内容↓'
            ))
            await app.send_group_message(tar, msg.removeprefix("跨群消息|"+data[1]+"|"))
            try:await app.send_message(group, MessageChain("跨群发送信息成功~"))
            finally:pass
        except AccountMuted:
            await app.send_friend_message(673457979, MessageChain(
                "哦豁，被禁言了",
                Face(name="doge"),
                "\n群号:",
                str(group.id),
                "\n欲回复消息:",
                msg.content,
                "\n发送人:[",
                str(mem.id),
                "]",
                mem.name
            ))
            await app.send_message(group, MessageChain("此群表示让我闭嘴(禁言)", Face(name='doge'), Image(path='res/a5.jpg')))
        except UnknownTarget:
            await app.send_message(group, MessageChain(
                At(mem.id)
                , "亲，这个群我还没进呢",
                Face(name='doge'),
                '\n或者说...这个群根本不存在',
                Face(name='汪汪')
            ))
