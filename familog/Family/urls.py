from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    # POST /families                ─ 가족 생성
    path('', views.FamilyCreateView.as_view(), name='family-create'),

    # GET  /families/<code>         ─ 가족 정보
    path('<str:code>/', views.FamilyDetailView.as_view(), name='family-detail'),

    # POST /families/<code>/join    ─ 가족 참여
    path('<str:code>/join/', views.FamilyJoinView.as_view(), name='family-join'),
]
