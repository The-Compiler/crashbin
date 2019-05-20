from django.apps import AppConfig


class CrashbinAppConfig(AppConfig):
    name = 'crashbin_app'

    def ready(self):
        # pylint: disable=unused-import
        import crashbin_app.signals  # noqa
