from cq_fun import *

text = rev_msg()
while True:
    text = rev_msg()
    print(text)
    if text['message_type'] == 'group' and text['message'] == 'Yeusint':
        send_msg({
            'type': "group",
            'id': str(text['group_id']),
            'msg': '滴滴滴！！！'
        })
