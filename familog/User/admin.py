# admin.py
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display       = ("id", "email", "nickname")   # 목록 컬럼
    list_display_links = ("email",)                    # 클릭해서 상세로
    search_fields      = ("email", "nickname")         # 검색
    ordering           = ("id",)                       # 기본 정렬
