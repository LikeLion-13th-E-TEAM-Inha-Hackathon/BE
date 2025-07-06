# Watering/admin.py
from django.contrib import admin
from .models import Watering


@admin.register(Watering)
class WateringAdmin(admin.ModelAdmin):
    list_display  = ("id", "plant", "member", "time")
    list_filter   = ("time",)
    autocomplete_fields = ("plant", "member")
