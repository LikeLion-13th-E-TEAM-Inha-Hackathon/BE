from django.contrib import admin
from django.urls import path

from . import views

from .views import get_today_question, QuestionView

urlpatterns = [
    path("families/<str:code>/questions/today", get_today_question, name="get_today_question"),
    path("families/<str:code>/questions", QuestionView.as_view(), name="question_view"),
]
