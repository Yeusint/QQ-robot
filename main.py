from graia.ariadne.entry import Ariadne, config
from graia.saya import Saya
from creart import create
App = Ariadne(config(2769124385, "INITKEY9N2rdEMQ"))
s = create(Saya)
with s.module_context():
    s.require("mod.gnc")
    s.require("mod.gsi")
    s.require("mod.music")
App.launch_blocking()
