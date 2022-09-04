from requests import get
from graia.ariadne.entry import Ariadne, GroupMessage, Group, MessageChain, Member, Face, Plain, DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

a = Channel.current()


@a.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix("点歌")]))
async def a(app: Ariadne, group: Group, msg: MessageChain = DetectPrefix("点歌")):
    await app.send_message(group, MessageChain(msg.display))
