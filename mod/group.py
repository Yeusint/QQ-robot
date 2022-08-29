from graia.ariadne.entry import Ariadne, Group, GroupMessage, Member, MessageChain, Image, At
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
        await app.send_message(group, MessageChain(str(get_admin_list(group.id)), Image(path="res/a1.png")))
        name = await app.get_member_profile(mem.id, group.id)
        name = name.nickname
