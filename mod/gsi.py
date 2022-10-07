from graia.ariadne.entry import Ariadne, MessageChain, Member, At, Image, GroupMessage, Group, Plain, Face, Friend
from graia.ariadne.exception import AccountMuted
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from fun import add_admin, is_member, del_admin, is_admin, add_node, del_node
a = Channel.current()


@a.use(ListenerSchema(listening_events=[GroupMessage]))
async def a(app: Ariadne, message: MessageChain, mem: Member, group: Group):
    try:
        if message.display[0:5] == "添加管理员" and mem.id == 673457979:
            m_list = await app.get_member_list(group.id)
            if message.display[5] == '@' and message.display[6:].rstrip().isdigit() is True:
                if add_admin(group.id, int(message.display[6:])):
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n已成功添加"),
                        At(int(message.display[6:])),
                        Plain("(" + message.display[6:] + ")为机器管理员"),
                        Face(name="汪汪"),
                        Image(path="res/a2.png")
                    ))
                else:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("错误：成员已添加"),
                        Face(name="doge"),
                        Image(path="res/a3.jpg")
                    ))
            elif message.display[5:].isdigit() is True:
                if is_member(m_list, int(message.display[5:])) is True:
                    if add_admin(group.id, int(message.display[5:])):
                        await app.send_message(group, MessageChain(
                            At(mem.id),
                            Plain("\n已成功添加"),
                            At(int(message.display[5:])),
                            Plain("(" + message.display[5:] + ")为机器管理员"),
                            Face(name="汪汪"),
                            Image(path="res/a2.png")
                        ))
                    else:
                        await app.send_message(group, MessageChain(
                            At(mem.id),
                            Plain("错误：成员已添加"),
                            Face(name="doge"),
                            Image(path="res/a3.jpg")
                        ))
                else:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("错误：无此成员"),
                        Face(name="doge"),
                        Image(path="res/a3.jpg")
                    )
                                           )
            else:
                pass
        elif message.display[0:5] == "删除管理员" and mem.id == 673457979:
            if message.display[5] == '@' and message.display[6:].rstrip().isdigit() is True:
                cache = del_admin(group.id, int(message.display[6:]))
                if cache == 0:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n从此以后,"),
                        At(int(message.display[6:])),
                        Plain("(" + message.display[6:] + ')就管不了我了'),
                        Face(name="汪汪"),
                        Image(path="res/a2.png")
                    ))
                elif cache == 1:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n错误,他可不是我的管理者"),
                        Face(name="doge"),
                        Image(path="res/a3.jpg")
                    ))
                elif cache == 2:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n我在这个群除了主人还没能管我的人"),
                        Face(name="汪汪"),
                        Image(path="res/a2.png")
                    ))
            elif message.display[5:].isdigit() is True:
                c = del_admin(group.id, int(message.display[5:]))
                if c == 0:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n从此以后,"),
                        Plain(message.display[5:] + '就管不了我了'),
                        Face(name="汪汪"),
                        Image(path="res/a2.png")
                    ))
                elif c == 1:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n错误,他可不是我的管理者"),
                        Face(name="doge"),
                        Image(path="res/a3.jpg")
                    ))
                elif c == 2:
                    await app.send_message(group, MessageChain(
                        At(mem.id),
                        Plain("\n我在这个群除了主人还没能管我的人"),
                        Face(name="汪汪"),
                        Image(path="res/a2.png")
                    ))
            else:
                pass
        elif message.display[:4] == "添加节点" and is_admin(group.id, mem.id):
            if add_node(message.display[4:]):
                await app.send_message(group, MessageChain(
                    At(mem.id),
                    Plain("节点添加成功~\n如是无用节点请及时删除"),
                    Face(name="doge"),
                    Image(path="res/a5.jpg")
                ))
            else:
                await app.send_message(group, MessageChain(
                    At(mem.id),
                    Plain("站点格式错误..."),
                    Face(name="emm"),
                    Plain(
                        "\n请将节点网址检查:\n" +
                        "1.请不要加协议头(http等)\n" +
                        "2.末尾不要有斜杠"
                    ),
                    Image(path="res/a6.jpg")
                ))
        elif message.display[:4] == "删除节点" and is_admin(group.id, mem.id):
            if del_node(message.display[4:]):
                await app.send_message(group, MessageChain(
                    At(mem.id),
                    Plain("节点删除成功~"),
                    Face(name="汪汪"),
                    Image(path="res/a2.png")
                ))
            else:
                await app.send_message(group, MessageChain(
                    At(mem.id),
                    Plain("删除失败..."),
                    Face(name="emm"),
                    Plain(
                        "\n原因可能是:\n" +
                        "1.删到不能再删了，只有一个了\n" +
                        "2.根本就没这节点"
                    ),
                    Image(path="res/a3.jpg")
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
