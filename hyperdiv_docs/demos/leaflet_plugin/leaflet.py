import os
import hyperdiv as hd


class leaflet(hd.Plugin):
    _assets_root = os.path.join(os.path.dirname(__file__), "assets")
    _assets = [
        "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
        "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
        "leaflet-plugin.js",
    ]

    zoom = hd.Prop(hd.Int, 13)
    lat = hd.Prop(hd.Float, 51.505)
    lng = hd.Prop(hd.Float, -0.09)

    def __init__(self, height=20, **kwargs):
        super().__init__(height=height, **kwargs)
