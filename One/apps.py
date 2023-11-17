from django.apps import AppConfig

class OneConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'One'

    def ready(self):
        
        import One.signals