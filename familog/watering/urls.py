from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # GET /families/<code>/watering/log
    path('log/', views.WateringLogListView.as_view(), name='watering-log'),
]
