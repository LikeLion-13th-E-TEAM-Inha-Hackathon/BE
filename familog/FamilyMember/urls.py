from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # GET /families/<code>/members
    path('', views.MemberListView.as_view(), name='member-list'),

    # PATCH /families/<code>/members/<id>/role
    path('<int:pk>/role/', views.MemberRoleUpdateView.as_view(),
         name='member-role-update'),

    # DELETE /families/<code>/members/<id>
    path('<int:pk>/', views.MemberDeleteView.as_view(), name='member-delete'),
]
