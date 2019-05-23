import logging
import pkgutil
import typing

from django.conf import settings


config = settings.CRASHBIN_CONFIG  # type: ignore


def _on_walk_error(name: str) -> None:
    raise ImportError("Failed to import plugin {}".format(name))


def load_plugins() -> None:
    """Import all plugin modules from ~/.crashbin/plugins."""
    prefix = 'crashbin_app.plugins.'
    plugin_path = config.HOMEDIR / 'plugins'
    for finder, full_name, _ispkg in pkgutil.walk_packages(
            path=[str(plugin_path)], prefix=prefix, onerror=_on_walk_error):
        name = full_name[len(prefix):]
        try:
            finder.find_module(full_name).load_module(full_name)
        except Exception:  # pylint: disable=broad-except
            logging.exception("Exception while loading plugin: %s", name)
        else:
            logging.info("Loaded plugin: %s", name)


def parse_hex_color(color: str) -> typing.Tuple[int, int, int]:
    """Parse a string like #rrggbb into three ints."""
    color = color.lstrip('#')
    r = int(color[:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:], 16)
    return r, g, b


def font_color(r: int, g: int, b: int) -> str:
    """Given three r/g/b ints, get a color name for a font color."""
    # https://www.w3.org/Graphics/Color/sRGB
    luminance = (0.2126*r + 0.7152*g + 0.0722*b) / 255
    return 'black' if luminance > 0.5 else 'white'
