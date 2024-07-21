from graia.ariadne.entry import Ariadne, config
from graia.saya import Saya
from creart import create
App = Ariadne(config(2769124385, "YHP_1145"))
s = create(Saya)
with s.module_context():
    s.require("mod.gnc")
    s.require("mod.gsi")
    s.require("mod.cgc")
    s.require("mod.music")
    s.require("mod.recall")
App.launch_blocking()
