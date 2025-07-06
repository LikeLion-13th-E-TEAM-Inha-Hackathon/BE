# Answer/admin.py
from django.contrib import admin
from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display  = ("id", "question", "member", "short_content")
    search_fields = ("member__user__nickname", "question__content", "content")

    @admin.display(description="content")
    def short_content(self, obj):
        return (obj.content[:30] + "...") if len(obj.content) > 30 else obj.content
