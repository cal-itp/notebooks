import os
import subprocess
import textwrap

from pathlib import Path
from typing import Mapping, Dict

from diagrams import Node

MAX_NODE_LINE_LENGTH = 30


class _TransitComponents(Node):
    """Base class for transit stack diagram nodes."""

    _type = "transit"
    _provider = "custom"

    _icon_dir = os.path.join(Path().absolute().parent, "transitstacks", "icons")
    _icon = None
    _height = 1.9
    fontcolor = "#ffffff"

    def __init__(self, label: str = "", **attrs: Dict):
        super().__init__(label, **attrs)
        # print(self.label)
        # TODO
        # Commented out for now because was becoming complicated
        # to link this up with the relationships
        # self.label = "\n".join(textwrap.wrap(self.label, MAX_NODE_LINE_LENGTH))
        # print(self.label)

    def _load_icon(self):

        full_icon_path = os.path.join(_TransitComponents._icon_dir, self._icon)
        if not os.path.exists(full_icon_path):
            print("couldn't find file", full_icon_path)
        elif full_icon_path.endswith(".svg"):
            _svg2png_file(full_icon_path)
            self._icon = self._icon.replace(".svg", ".png")
            return self._load_icon()
        else:
            return full_icon_path


class Default(_TransitComponents):
    _icon = "default.png"


class Audio(_TransitComponents):
    _icon = "noun_Volume_3408323.svg"


class Avl(_TransitComponents):
    _icon = "noun_GPS_3075574.svg"


class Cloudsoftware(_TransitComponents):
    _icon = "noun_Cloud Computing_204953.svg"


class Dashboard(_TransitComponents):
    _icon = "alerting.svg"


class Datastream(_TransitComponents):
    _icon = "noun_cloud storage_1175784.svg"


class Farebox(_TransitComponents):
    _icon = "noun_insert coin_885351.svg"


class Gps(_TransitComponents):
    _icon = "noun_GPS_3075574.svg"


class Gtfs(_TransitComponents):
    _icon = "noun_iphone x transit app_2590390.svg"


class Mobileticketing(_TransitComponents):
    _icon = "noun_Public transport pass_1185962.svg"


class Onboardsensor(_TransitComponents):
    _icon = "noun_sensor_2495154.svg"


class Onboardcomputer(_TransitComponents):
    _icon = "noun_computer tower_1423132.svg"


class Overaircoms(_TransitComponents):
    _icon = "noun_wifi_2390548.svg"


class Payments(_TransitComponents):
    _icon = "noun_Payment process_1877943.svg"


class Scheduling(_TransitComponents):
    _icon = "noun_Time Work_1136908.svg"


class Server(_TransitComponents):
    _icon = "noun_data server_1803518.svg"


class Signage(_TransitComponents):
    _icon = "noun_signage_1559416.svg"


class Ticketing(_TransitComponents):
    _icon = "noun_vending machine_3223884.svg"


def _svg2png_file(
    filename: str,
    opts: Mapping[str, str] = {"-output-width": "256", "-output-width": "256"},
) -> None:
    """Converts an SVG file to a PNG file using Cairo SVG.

    Args:
        filename: filename to process
        opts: dictionary of options for svg to png convertion
    """
    path_dest = filename.replace(".svg", ".png")
    if os.path.exists(path_dest):
        return
    try:
        subprocess.call(
            ["cairosvg", filename, "-f", "png", "-output-width", *opts, "-o", path_dest]
        )
    except FileNotFoundError:
        print("try installing cairo svg")
