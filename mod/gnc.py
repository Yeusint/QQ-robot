from graia.ariadne.entry import (
    Ariadne,
    Group,
    GroupMessage,
    Member,
    MessageChain,
    Image,
    At,
    Face
)
from graia.ariadne.exception import AccountMuted
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.element import Xml
from fun.cache_var import start_time
from time import time, localtime, strftime
from fun import get_speed, get_speed_result, get_admin_list, is_admin, mute_time
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
        elif message.display == "运行时间":
            await app.send_message(group, MessageChain(
                At(mem),
                "获取成功~\n启动时间:",
                strftime("%m月%d日%H时%M分%S秒", localtime(start_time)),
                "\n当前时间:",
                strftime("%m月%d日%H时%M分%S秒"),
                "\n已启动时间:",
                mute_time(int(time()-start_time))
            ))
        elif message.display == 'cs':
            await app.send_message(group, MessageChain(Xml("""
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<msg serviceID="1" templateID="1" action="web" brief="邪少QQXML论坛" sourceMsgId="0" url="https://qun.qq.com/homework/features/v2/index.html?_wv=1027&amp;_bid=3089&amp;#src=2&amp;hw_id=2002159585984144&amp;puin=3241172150&amp;hw_type=0&amp;need_feedback=0&amp;gc=711695859&amp;from=obj" flag="3" adverSign="0" multiMsgFlag="0"><item layout="2" advertiser_id="0" aid="0"><picture cover="https://ae01.alicdn.com/kf/Ue8b39fcb16b440b0be3a43ee4fbfa00dO.png" w="0" h="0" /><title>2月25日作业</title><summary>邪少QQXML论坛</summary></item><source name="邪少QQXML论坛" icon="" action="" appid="-1" /></msg>
"""
                                                           )))
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
        elif message.display == '停止' and mem.id == 673457979:
            await app.send_message(group, MessageChain("注意: 机器已停止运行！但后台未关闭！"))
            exit(520)
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
