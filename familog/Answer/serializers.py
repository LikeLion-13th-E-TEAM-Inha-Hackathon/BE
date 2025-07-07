from rest_framework import serializers
from .models import Answer

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["content"]

class AnswerListSerializer(serializers.ModelSerializer):
    memberId = serializers.IntegerField(source="member.id")
    nickname = serializers.CharField(source="member.user.nickname")

    class Meta:
        model = Answer
        fields = ["memberId", "nickname", "content"]
