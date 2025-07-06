# FamilyMember/admin.py
from django.contrib import admin
from .models import FamilyMember


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display  = ("id", "family", "user", "role")
    list_filter   = ("role", "family")
    search_fields = ("user__email", "user__nickname", "family__code")
