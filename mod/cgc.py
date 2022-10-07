import graia.ariadne.exception
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import Ariadne, GroupMessage, Group, MessageChain, Member, DetectPrefix, Source, Face
from fun import is_group
c = Channel.current()

@c.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix("跨群消息|")]))
async def a(app: Ariadne, group: Group, mem: Member, msg: Source):
    data = msg.display.split("|")
    if len(data) == 3 and is_group(await app.get_group_list(), group.id) and data[1].isdigit():
        tar = int(data[1])
        try:
            await app.send_group_message(tar, MessageChain(data[2]))
        except graia.ariadne.exception.AccountMuted:
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
        try:
            await app.send_message(group, MessageChain("跨群发送信息成功~"))
        except graia.ariadne.exception.AccountMuted:
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
