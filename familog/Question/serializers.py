from rest_framework import serializers
from .models import Question, QuestionPool

from rest_framework import serializers
from .models import Question, QuestionPool

class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField(source='q_date', read_only=True)
    content = serializers.CharField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    code = serializers.CharField(source='family.code', read_only=True)  # ✅ 이거 추가

    class Meta:
        model = Question
        fields = ("id", "date", "content", "is_completed", "code")  # ✅ 포함시켜야 함


class QuestionPoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPool
        fields = ("id", "content")

    def validate_content(self, value):
        if QuestionPool.objects.filter(content=value).exists():
            raise serializers.ValidationError("이미 존재하는 질문입니다.")
        return value
