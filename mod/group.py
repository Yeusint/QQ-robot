from graia.ariadne.entry import Ariadne, Group, GroupMessage, Member, MessageChain, Image
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
c = Channel.current()


@c.use(ListenerSchema(listening_events=[GroupMessage]))
async def c(app: Ariadne, group: Group, mem: Member, message: MessageChain):
    if message.display == "a":
        await app.send_message(group, MessageChain(Image(url="https://q.qlogo.cn/g?b=qq&nk=" + str(mem.id) + "&s=0")))
    elif message.display == "ln":
        await app.send_message(group, MessageChain())
