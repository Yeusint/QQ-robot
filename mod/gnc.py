from graia.ariadne.entry import (
    Ariadne,
    Group,
    GroupMessage,
    Member,
    MessageChain,
    Image,
    At,
    Face,
    MultimediaElement
)
from graia.ariadne.exception import AccountMuted
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from fun import get_speed, get_speed_result, get_admin_list, is_admin
c = Channel.current()


@c.use(ListenerSchema(listening_events=[GroupMessage]))
async def c(app: Ariadne, group: Group, mem: Member, message: MessageChain):
    try:
        if message.display == "a":
            await app.send_message(group,MessageChain(Image(url="https://q.qlogo.cn/g?b=qq&nk=" + str(mem.id) + "&s=0")))
        elif message.display == "查看机器网络状态" and is_admin(group.id, mem.id):
            await app.send_message(group,MessageChain(At(mem), get_speed_result(get_speed())))
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
        elif message.display == "获取群列表":
            _list = await app.get_group_list()
            result = ''
            for i in range(len(_list)):result += _list[i].name + '(' + str(_list[i].id) + ')\n'
            await app.send_message(group, MessageChain(
                At(mem.id),
                "获取成功~\n------------------\n",
                result,
                '---------------\n列出完毕~',
                Face(name='花朵脸'),
                Image(path="res/a2.png")
            ))
        elif message.display == 'cs':
            await app.send_message(group, MessageChain(MultimediaElement(path="res/y.mp4")))
        elif message.display == '翻译':
            await app.send_message(group, MessageChain(
                "[翻译]\n"
                "---------------------------\n"
                "翻译+目标语种代码[空格]需要翻译的文本\n"
                "---------------------------\n"
                "例：翻译zh apple\n"
                "语种代码参考↓\n",
                Image(path="res/lan.png")
            ))
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
    except PermissionError:await app.send_message(group, MessageChain("嘤嘤嘤,俺没权限~", Face(name="doge"), Image(path="res/a7.gif")))
