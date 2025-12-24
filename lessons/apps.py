from django.apps import AppConfig


class LessonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lessons"

    def ready(self) -> None:
        # Import signals to register handlers once the app is ready.
        from . import signals  # noqa: F401


