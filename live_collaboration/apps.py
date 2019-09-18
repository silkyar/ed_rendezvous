from django.apps import AppConfig


class LiveCollaborationConfig(AppConfig):
    name = 'live_collaboration'

    def ready(self):
        import live_collaboration.signals
