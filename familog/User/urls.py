from django.urls import path
from .views import SignupView, LoginView, UserDeleteView, UserDetailView

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("<int:pk>/", UserDetailView.as_view()),      # 🔹 GET /users/<id>/
    path("<int:pk>/delete/", UserDeleteView.as_view())  # 🔹 DELETE /users/<id>/delete/
]
