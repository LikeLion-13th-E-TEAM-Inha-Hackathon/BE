# Question/admin.py
from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display  = ("id", "family", "q_date", "is_completed")
    list_filter   = ("is_completed", "q_date")
    search_fields = ("family__code", "content")
