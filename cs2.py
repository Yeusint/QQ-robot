import requests
import json
from datetime import date

txt = open("tidy.txt", 'r', encoding='UTF-8').read()
tidy_name = txt[0:txt.find('_')].splitlines()
tidy_code = txt[txt.find('_') + 2:len(txt)].splitlines()
headers = {
        'Accept': 'text/html,'
                  'application/xhtml+xml,'
                  'application/xml;q=0.9,'
                  'image/avif,'
                  'image/webp,'
                  'image/apng,'
                  '*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_187fda34c81598ec29ebc4da675267cc=1647742632;'
                  ' ASPSESSIONIDQUQRTCAB=CBILGFEDILOKGAGDKOMNDGLI;'
                  ' ASPSESSIONIDSUSQRADB=JNHPGFEDLGLFJILJFDJIENJD;'
                  ' ASPSESSIONIDSWSSTDCA=BPHJGFEDECALNBDMFKNJLHCE;'
                  ' ASPSESSIONIDQUSTQBBB=BFHHFFEDBNFCGMNDHKKHNAMF;'
                  ' ASPSESSIONIDQURQTDAA=DLHNFFEDNNDFKMPHKFHJIJAC;'
                  ' ASPSESSIONIDSWSTTAAA=BCIJFFEDBAFCLMIFNJJDGALK;'
                  ' ASPSESSIONIDQWQRSADB=NNHDGFEDJNHPKIKBOHPKBEJJ;'
                  ' ASPSESSIONIDQWSQTAAA=MFIBFFEDOBHNEJGGLCEGNBCC;'
                  ' ASPSESSIONIDQURSRBAD=HIILFFEDAJOMGKIIEGHIDOOM;'
                  ' ASPSESSIONIDQWSTQAAB=KGBENIEDLIFHLGCGIOLJKBLM;'
                  ' ASPSESSIONIDSUSTRCAA=AINBFFEDPIGLHDHNDBNBNBLE;'
                  ' ASPSESSIONIDSWTSTCAB=FBLJFFEDJPFKMFIAPGEFNKKB;'
                  ' ASPSESSIONIDSURTTCBA=FNAEGFEDKHBPIPELDEDAIKKC;'
                  ' ASPSESSIONIDCUQSSCDD=BMBGFFEDFHKGIHFHHECJMHAF;'
                  ' Hm_lpvt_187fda34c81598ec29ebc4da675267cc=1647751523',
        'Host': 'api.help.bj.cn',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/86.0.4240.198 Safari/537.36'
    }
a = input('请输入城市')
b = json.loads(requests.request(
    'get', 'https://api.help.bj.cn/apis/weather6d/?id=' + tidy_code[tidy_name.index(a)], headers=headers
).text)['data']
print(b['forecast'])
result = '[最近六日天气]' \
    '\n月份：' + str(date.today().month) + '月' \
    '\n城市：' + b['city'] +\
    '\n--------------------------' \
    '\n日期：' + b['yesterday']['date'] +\
    '\n气温：' + b['yesterday']['templow'] + '°C-' + b['yesterday']['temphigh'] + '°C' \
    '\n风力：' + b['yesterday']['wind'] + b['yesterday']['windforce'] +\
    '\n--------------------------'
i = 0
while i < len((b['forecast'])):
    result = result + \
        '\n日期：' + b['forecast'][i]['date'] + \
        '\n气温：' + b['forecast'][i]['templow'] + '°C-' + b['forecast'][i]['temphigh'] + '°C' \
        '\n风力：' + b['forecast'][i]['wind'] + b['forecast'][i]['windforce'] + \
        '\n--------------------------'
    i += 1
result = result + "\n温馨提示：" + b['life']
print(result)
