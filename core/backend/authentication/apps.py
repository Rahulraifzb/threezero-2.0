from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.backend.authentication'

    def ready(self):
        import core.backend.authentication.signals
