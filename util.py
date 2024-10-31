import os
import json

cfgfile = "settings.json"

def load_settings():
    if os.path.exists(cfgfile):
        with open(cfgfile, "r") as f:
            return json.load(f)
    return None


def save_settings(widget):
    position = widget.pos()
    size = widget.size()
    all_data = {"position" : {"x": position.x(), "y": position.y()}}
    all_data["size"] = {"width": size.width(), "height": size.height()}
    all_data["tickers"] = widget.tickers
    with open(cfgfile, "w") as f:
        json.dump(all_data, f)

