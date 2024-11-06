from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoderrAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coderr_app'


    def ready(self):
        """
        Registriert das `create_guest_accounts` Signal mit dem `post_migrate` Ereignis,
        sodass nach jeder Migration automatisch Gast-Accounts erstellt werden.
        """
        from .signals import create_guest_accounts
        post_migrate.connect(create_guest_accounts, sender=self)