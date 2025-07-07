from django.urls import path
from .views import AnswerView, MyAnswerUpdateView

urlpatterns = [
    path("<int:id>/answers", AnswerView.as_view(), name="answer-view"),           # GET, POST
    path("<int:id>/answers/me", MyAnswerUpdateView.as_view(), name="answer-update"),  # PATCH
]