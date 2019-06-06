import logging
import pkgutil
import attr

from django.conf import settings
from django.http import HttpRequest
from django.utils.http import is_safe_url

config = settings.CRASHBIN_CONFIG  # type: ignore


def _on_walk_error(name: str) -> None:
    raise ImportError(f"Failed to import plugin {name}")


def back_redirect_ok(request: HttpRequest):
    if "back" not in request.GET:
        return False
    return is_safe_url(request.GET["back"], allowed_hosts=None)


def load_plugins() -> None:
    """Import all plugin modules from ~/.crashbin/plugins."""
    prefix = "crashbin_app.plugins."
    plugin_path = config.HOMEDIR / "plugins"
    for finder, full_name, _ispkg in pkgutil.walk_packages(
        path=[str(plugin_path)], prefix=prefix, onerror=_on_walk_error
    ):
        name = full_name[len(prefix) :]
        try:
            finder.find_module(full_name).load_module(full_name)
        except Exception:  # pylint: disable=broad-except
            logging.exception("Exception while loading plugin: %s", name)
        else:
            logging.info("Loaded plugin: %s", name)


@attr.s
class Color:

    r: int = attr.ib()
    g: int = attr.ib()
    b: int = attr.ib()

    @classmethod
    def from_hex(cls, color: str):
        color = color.lstrip("#")
        return cls(r=int(color[:2], 16), g=int(color[2:4], 16), b=int(color[4:], 16))

    def font_color(self) -> str:
        """Get a color name for a font color."""
        # https://www.w3.org/Graphics/Color/sRGB
        luminance = (0.2126 * self.r + 0.7152 * self.g + 0.0722 * self.b) / 255
        return "black" if luminance > 0.5 else "white"
