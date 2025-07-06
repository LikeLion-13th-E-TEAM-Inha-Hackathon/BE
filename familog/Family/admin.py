# Family/admin.py
from django.contrib import admin
from .models import Family


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display  = ("code", "name", "seeds")
    search_fields = ("code", "name")
