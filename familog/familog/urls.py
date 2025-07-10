from django.contrib import admin
from django.urls import path, include 
from django.urls import re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Familog API",
        default_version="v1",
        description="Familog Swagger Docs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

# 🔐 Swagger에 JWT 입력창 나오게 하기 위한 설정
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT 토큰을 입력하세요. 예: Bearer <your_access_token>',
        }
    },
    'USE_SESSION_AUTH': False,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # 로그인
    path('users/', include('User.urls')),

    # 가족 관련
    path('families/', include('Family.urls')),
    path('families/<str:code>/members/', include('FamilyMember.urls')),
    path('families/<str:code>/plant/', include('Plant.urls')),
    path('families/<str:code>/questions/', include('Question.urls')),

    # 답변 관련
    path('questions/', include('Answer.urls')),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
]
