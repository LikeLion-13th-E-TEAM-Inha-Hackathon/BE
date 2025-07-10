from rest_framework import serializers
from .models import Question, QuestionPool


# ────────────────────────────────────────────────────────────
# ✅ 오늘의 질문 / 질문 서랍용 Serializer (GET 응답)
# ────────────────────────────────────────────────────────────
class QuestionSerializer(serializers.ModelSerializer):
    id           = serializers.IntegerField(read_only=True)
    date         = serializers.DateField(source='q_date', read_only=True)
    content      = serializers.CharField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Question
        fields = ("id", "date", "content", "is_completed")


# ────────────────────────────────────────────────────────────
# ✅ 질문 추가용 Serializer (POST /questions)
# ────────────────────────────────────────────────────────────
class QuestionPoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPool
        fields = ("id", "content")
