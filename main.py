from graia.ariadne.entry import Ariadne, config, WebsocketClientConfig, HttpClientConfig
from graia.saya import Saya
from creart import create
App = Ariadne(config(2769124385,
                     "INITKEYvxsoCYVE",
                     HttpClientConfig(host="http://127.0.0.1:8080"),
                     WebsocketClientConfig(host="http://127.0.0.1:8080")))
s = create(Saya)
with s.module_context():
    s.require("mod.group")
App.launch_blocking()
