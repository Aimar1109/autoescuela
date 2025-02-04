from django.db.models.signals import post_migrate
from django.apps import AppConfig

class PracticasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'practicas'

    def ready(self):
        from .utils import setup_groups
        post_migrate.connect(setup_groups, sender=self)
