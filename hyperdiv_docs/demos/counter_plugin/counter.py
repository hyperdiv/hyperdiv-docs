import os
import hyperdiv as hd


class counter(hd.Plugin):
    _assets_root = os.path.join(os.path.dirname(__file__), "assets")
    _assets = ["*"]

    count = hd.Prop(hd.Int, 0)


class boxy_counter(hd.Plugin, hd.Boxy):
    _name = "counter"
    _classes = ["box"]
    _assets_root = os.path.join(os.path.dirname(__file__), "assets")
    _assets = ["*"]

    count = hd.Prop(hd.Int, 0)
