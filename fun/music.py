from hashlib import md5
from time import time
from requests import get
#from json import loads


def get_kugou(song_name: str, mode: int,cookie: dict)-> str:
    """
    mode_num_explain\n
    1 find->list\n
    2 song->dict\n
    3 song->url\n
    """
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
    f = get(r).json()
    g = get(
        f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&dfid={cookie["dfid"]}&appid=1014&mid={cookie["mid"]}&platid=4&encode_album_audio_id={f["data"]["lists"][0]["EMixSongID"]}&_=1672713853357',
        cookies=cookie
    ).json()['data']['play_url']
    return g
