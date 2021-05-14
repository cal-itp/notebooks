from typing import Collection
from colour import Color


def contrast_color(hexcolor: str) -> str:
    """Calculates if font should be B or W based on luminance
    and W3C accessibility recommendations.
      https://www.w3.org/TR/WCAG20/

    Solution based on:
      https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color

    Args:
        hexcolor (str): hexidecimal color code

    Returns:
        best hexidecimal font color
    """

    c = Color(hexcolor)

    # 0.179 seemed too low even though
    # it is based on W3C guidance
    # if c.luminance > 0.179:
    if c.luminance > 0.4:

        return "#000000"

    return "#ffffff"


def _adjust_hex(hexcolor: str, brightness_adj: float = 1.0, saturation_adj=1.0) -> str:

    c = Color(hexcolor)
    c.luminance = min(c.luminance * brightness_adj, 1)
    c.saturation = min(c.saturation * saturation_adj, 1)
    return c.hex


def color_ramp(
    color_ramp: Collection,
    brightness_adj: float = 1,
    saturation_adj: float = 1,
    quantity: int = None,
) -> Collection[str]:
    """[summary]

    Example usage::

        ramp = color_ramp(
            color_ramp=cc.glasbey_cool,
            saturation_adj = 0.5,
            brightness_adj= 1.2,
            quantity = 16
        )

    Args:
        color_ramp (Collection, optional): [description]. Defaults to cc.glasbey_cool.
        brightness_adj (float, optional): [description]. Defaults to BRIGHTNESS_ADJ.
        quantity (int, optional): [description]. Defaults to None.

    Returns:
        List of colors with noted adjustments and necessary quantity.
    """
    from math import ceil

    if brightness_adj or saturation_adj:
        color_ramp = [
            _adjust_hex(c, brightness_adj=brightness_adj, saturation_adj=saturation_adj)
            for c in color_ramp
        ]
    if quantity > len(color_ramp):
        color_ramp = color_ramp * ceil(quantity / len(color_ramp))
    if quantity:
        color_ramp = color_ramp[:quantity]
    return color_ramp


def show_ramp(hex_list):
    """Shows color ramp as a matplotlib grid.

    Args:
        hex_list ([type]): [description]
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba_array
    import math

    # find closest square for n numbers
    n = len(hex_list)
    _width = math.floor(math.sqrt(n))
    while n % _width > 0:
        _width -= 1
    _height = n / _width

    plt.imshow(to_rgba_array(hex_list).reshape(_height, _width, 4))
    plt.show()
    return
