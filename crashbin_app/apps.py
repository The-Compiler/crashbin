import logging

from django.apps import AppConfig


class CrashbinAppConfig(AppConfig):
    name = "crashbin_app"

    def ready(self):
        logging.basicConfig(level=logging.INFO)
        # pylint: disable=unused-import
        import crashbin_app.signals  # noqa
        from crashbin_app import utils

        utils.load_plugins()
