from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # GET /families/<code>/plant
    path('', views.PlantDetailView.as_view(), name='plant-detail'),

    # POST /families/<code>/plant/water
    path('water/', views.PlantWaterView.as_view(), name='plant-water'),
]
