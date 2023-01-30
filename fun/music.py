from hashlib import md5
from time import time
from requests import get


def get_kugou(song_name: str)-> list:
    _md5 = md5()
    params = [
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
        "appid=1014",
        "bitrate=0",
        f"clienttime={int(time() * 1000)}",
        "clientver=1000",
        "dfid=-",
        "filter=10",
        "inputtype=0",
        "iscorrection=1",
        "isfuzzy=0",
        f"keyword={song_name}",
        "mid=-",
        "page=1",
        "pagesize=30",
        "platform=WebFilter",
        "privilege_filter=0",
        "srcappid=2919",
        "token=",
        "userid=0",
        "uuid=",
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    ]
    info = "".join(params)
    _md5.update(info.encode(encoding='utf-8'))
    signature = _md5.hexdigest()
    del params[0]
    del params[-1]
    params.append(f"signature={signature}")
    r = "https://complexsearch.kugou.com/v2/search/song?"
    i = 0
    while i < len(params):
        r += params[i]
        r += '&'
        i += 1
    return get(r).json()['data']['lists']

def song_data(music_id:str, source: str,cookie:dict=None)-> dict:
    """
    :param music_id: id
    :param source:kugou|qq|nes
    :param cookie:user_data
    :return: music_info
    """
    if source == "kugou":
        g = get(
            f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&dfid={cookie["dfid"]}&appid=1014&mid={cookie["mid"]}&platid=4&encode_album_audio_id={music_id}&_=1672801556353',
            cookies=cookie
        ).json()['data']
        return g
    return {}
