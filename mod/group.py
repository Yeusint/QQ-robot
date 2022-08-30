from graia.ariadne.entry import Ariadne, Group, GroupMessage, Member, MessageChain, Image, At, Face
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from fun import get_speed, get_speed_result, get_admin_list
c = Channel.current()


@c.use(ListenerSchema(listening_events=[GroupMessage]))
async def c(app: Ariadne, group: Group, mem: Member, message: MessageChain):
    if message.display == "a":
        await app.send_message(group, MessageChain(Image(url="https://q.qlogo.cn/g?b=qq&nk=" + str(mem.id) + "&s=0")))
    elif message.display == "ln" and mem.id == 673457979:
        await app.send_message(group, MessageChain(At(mem), "\n--------------------\n", get_speed_result(get_speed())))
    elif message.display == "获取管理员列表":
        m_list = await app.get_member_list(group.id)
        admin_list = get_admin_list(group.id, m_list)
        if admin_list[len(admin_list)-1] == 0:
            admin_list.remove(0)
            await app.send_message(group, MessageChain(admin_list))
        elif admin_list[len(admin_list)-1] == 1:
            admin_list.remove(1)
            result = [
                At(mem.id),
                "\n一共有",
                str(len(admin_list)//2),
                "位管理员\n",
                "----------------------\n"
            ]+admin_list+[
                "----------------------\n",
                "列出完毕",
                Face(name='汪汪')
            ]
            await app.send_message(group, MessageChain(result))
    elif message.display[0:5] == "添加管理员" and mem.id == 673457979:

