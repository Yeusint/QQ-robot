from graia.ariadne.entry import (
    Ariadne,
    Group,
    GroupMessage,
    Member,
    MessageChain,
    Image,
    At,
    Face,
    Voice,
    Source
)
from graia.ariadne.exception import AccountMuted
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from fun import get_speed, get_speed_result, get_admin_list, is_admin
from graiax import silkcoder
from random import randint
from json import loads, dumps
c = Channel.current()


@c.use(ListenerSchema(listening_events=[GroupMessage]))
async def c(app: Ariadne, group: Group, mem: Member, message: MessageChain, s: Source):
    try:
        if message.display == "a":
            await app.send_message(group,MessageChain(Image(url="https://q.qlogo.cn/g?b=qq&nk=" + str(mem.id) + "&s=0")))
        elif message.display == "查看机器网络状态" and is_admin(group.id, mem.id):
            await app.send_message(group,MessageChain(At(mem), "\n--------------------\n", get_speed_result(get_speed())))
        elif message.display == "获取管理员列表":
            m_list = await app.get_member_list(group.id)
            admin_list = get_admin_list(group.id, m_list)
            if admin_list[len(admin_list) - 1] == 0:
                admin_list.remove(0)
                await app.send_message(group, MessageChain(admin_list))
            elif admin_list[len(admin_list) - 1] == 1:
                admin_list.remove(1)
                result = [
                             At(mem.id),
                             "\n一共有",
                             str(len(admin_list) // 2),
                             "位管理员\n",
                             "----------------------\n"
                         ] + admin_list + [
                             "----------------------\n",
                             "列出完毕",
                             Face(name='汪汪')
                         ]
                await app.send_message(group, MessageChain(result))
        elif message.display == 'cs':
            v = await silkcoder.async_encode(
                open("F:\\Yeuisnt\\mirai-robot\\res\\v.flac", 'rb').read(),
                audio_format='flac')
            await app.send_message(group, MessageChain(Voice(data_bytes=v, length=320)))
        elif message.display == "c-" and is_admin(group.id, mem.id):
            await app.send_message(group, MessageChain("开始同步~"))
            r = open("res/data.json", "r")
            cache = loads(r.read())
            r.close()
            g = await app.get_group_list()
            cache['group_data'] = {}
            cache['friend_data'] = []
            for i in range(len(g)):
                m = await app.get_member_list(g[i])
                cache['group_data'][g[i].id] = []
                for i_ in range(len(m)):
                    cache['group_data'][g[i].id].append(m[i_].id)
            g = await app.get_friend_list()
            for i in range(len(g)):
                cache['friend_data'].append(g[i].id)
            open("res/data.json", "w").write(dumps(cache))
            await app.send_message(group, MessageChain("同步完成~\n一共", str(len(cache['group_data'])), "个群\n拥有", str(len(cache['friend_data'])), "个好友"))
        elif message.display == "ch":await app.recall_message(s, target=group)
    except AccountMuted:
        await app.send_friend_message(673457979, MessageChain(
            "哦豁，被禁言了",
            Face(name="doge"),
            "\n群号:",
            str(group.id),
            "\n欲回复消息:",
            message.content,
            "\n发送人:[",
            str(mem.id),
            "]",
            mem.name
        ))
    except PermissionError:
        await app.send_message(group, MessageChain("嘤嘤嘤,俺没权限~", Face(name="doge"), Image(path="res/a7.gif")))
