import os
import hyperdiv as hd


class counter(hd.Plugin):
    _name = "counter"
    _assets_root = os.path.join(os.path.dirname(__file__), "assets")
    _assets = ["*"]

    count = hd.Prop(hd.Int, 0)


class boxy_counter(counter, hd.Boxy):
    _classes = ["box"]
