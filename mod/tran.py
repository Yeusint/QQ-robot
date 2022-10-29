from graia.ariadne.entry import Ariadne, Group, MessageChain, GroupMessage, DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from fun import translate, loads, dumps
c = Channel.current()

@c.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix("翻译")]))
async def a(app: Ariadne, g: Group, msg:MessageChain=DetectPrefix("翻译")):
    lan:str = loads(open("res/data.json", 'r').read())["language"]
    lan:list=lan.split(',')
    if msg.display[:msg.display.find(' ')] in lan:
        await app.send_message(g, MessageChain(
            '原文:',
            msg.display[msg.display.find(' ')+1:],
            '\n译文:',
            translate(msg.display[msg.display.find(' ')+1:], msg.display[:msg.display.find(' ')])
        ))
    else:
        pass
