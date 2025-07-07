from django.contrib import admin
from django.urls import path

from . import views

from .views import get_today_question, QuestionView

urlpatterns = [
    path("today", get_today_question), 
    path("", QuestionView.as_view()),
]
