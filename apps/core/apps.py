from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Arden's Bank"
    name = "apps.core"

    def ready(self) -> None:
        from . import signals
