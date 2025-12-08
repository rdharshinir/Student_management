from django.apps import AppConfig


class ExamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exams'

    def ready(self):
        # Ensure SystemConfig singleton exists when app starts
        try:
            from .models import SystemConfig
            SystemConfig.get_solo()
        except Exception:
            # avoid raising during migrations/initialization; fail silently
            pass


