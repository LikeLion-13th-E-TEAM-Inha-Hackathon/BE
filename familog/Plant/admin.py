# Plant/admin.py
from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display  = ("id", "family", "type", "grow_level", "last_watered")
    list_filter   = ("type",)

    search_fields = ("family__code", "type")   # family 코드·식물 타입으로 자동완성 검색
