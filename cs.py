from requests import get
print(get("https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=513463a335605f4597c06afd5548c0da").text)
