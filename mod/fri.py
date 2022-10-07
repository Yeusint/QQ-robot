from graia.ariadne.entry import Friend, Ariadne, MessageChain, FriendMessage
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from json import dumps
c = Channel.current()

@c.use(ListenerSchema(listening_events=[FriendMessage]))
async def a(app: Ariadne, f: Friend, msg:MessageChain):
    await app.send_message(f, MessageChain(msg.content))
