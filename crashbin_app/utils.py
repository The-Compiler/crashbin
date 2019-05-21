import logging
import pkgutil

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
