from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoderrAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coderr_app'


    def ready(self):
        from .signals import create_guest_accounts
        post_migrate.connect(create_guest_accounts, sender=self)