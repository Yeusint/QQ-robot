from graia.ariadne.entry import Ariadne, GroupRecallEvent, MessageChain
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
c = Channel.current()


@c.use(ListenerSchema(listening_events=[GroupRecallEvent]))
async def a(app: Ariadne, g: GroupRecallEvent):
    if g.author_id not in await app.get_bot_list():
        k = await app.get_message_from_id(g.message_id, target=g.group)
        await app.send_message(g.group, MessageChain(k.message_chain.content))
    else:
        pass
