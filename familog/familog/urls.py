"""
URL configuration for familog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

## Swagger 적용
from django.urls import re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Familog API",
        default_version="v1",
        description="Familog Swagger Docs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],  # 이 줄 없어도 되긴 함
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
    
    # 로그인 => 1 (진 파트)
    path('users/', include('User.urls')),
    
    # 진 파트 => 2 3 4 
    path('families/', include('Family.urls')), 
    path('families/<str:code>/members/', include('FamilyMember.urls')),
    path('families/<str:code>/plant/',        include('Plant.urls')),

    # 지윤님 파트 => 5 6
    
    
    # Swagger url
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    
]
