from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'
    
    def ready(self):
        import board.signals  # 시그널이 정의된 파일
