from django.apps import AppConfig


class EsnPolimiMgmtConfig(AppConfig):
    name = "esnpolimi_mgmt"

    def ready(self):
        import esnpolimi_mgmt.signals  # noqa F401
