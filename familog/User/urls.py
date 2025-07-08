# User/urls.py

from django.urls import path
from .views import SignupView, LoginView, UserDeleteView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path("<int:pk>/", UserDeleteView.as_view(), name="user-delete"),  # 회원 탈퇴
]
