from django.apps import AppConfig

class QuestionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Question"

    def ready(self):
        import Question.signals  # ← signals.py를 불러와서 자동 실행 연결
