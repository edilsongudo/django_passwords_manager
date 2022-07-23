from django.apps import AppConfig


class PassmanagerConfig(AppConfig):
    name = 'passmanager'

    def ready(self):
        import passmanager.signals
