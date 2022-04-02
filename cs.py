import requests
import json


print('请输入查询歌曲')
t = input()
html = requests.get(
    'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=' + t + '&page=1&pagesize=20&showtype=1'
)
music_search = json.loads(html.text)
i = 0
_hash = ['', '', '', '', '', '', '', '', '', '', ]
name = ''
while i < 10:
    _hash[i] = music_search['data']['info'][i]['hash']
    name = name + music_search['data']['info'][i]['filename'] + '\n'
    i += 1
print(_hash)
print(name)
print('请输入序号')
t = input()
if t.isdigit() is False:
    print('请输入序号！')
    exit()
elif int(t) < 0 or int(t) > 10:
    print('请输入正确序号！')
    exit()
_hash = _hash[int(t)]
html = requests.get("http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=" + _hash)
music_search = json.loads(html.text)
result = music_search['url']
if result == '':
    print('此为付费歌曲，无法播放！')
else:
    print(result)
