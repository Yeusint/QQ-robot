from graia.ariadne.entry import Ariadne, config, WebsocketClientConfig
from graia.saya import Saya
from creart import create
App = Ariadne(config(2769124385, "770308", WebsocketClientConfig("ws://1.117.108.106:80")))
s = create(Saya)
with s.module_context():
    s.require("mod.gnc")
    s.require("mod.gsi")
    s.require("mod.recall")
    s.require("mod.cgc")
App.launch_blocking()
