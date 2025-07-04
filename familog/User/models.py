from django.db import models

# Create your models here.
# 임시 => 추후 JWT 기반으로 
class User(models.Model):
    """커스텀 사용자 이메일 로그인"""
    username = None                      # 기본 username 제거
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []      # createsuperuser 시 email·password만

    def __str__(self) -> str:
        return f"{self.nickname}({self.email})"