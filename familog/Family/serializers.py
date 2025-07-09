# families/serializers.py
from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import Family


def _generate_code() -> str:
    """영문 대문자+숫자 8자리 초대 코드 생성 (중복 시 재시도)"""
    while True:
        code = get_random_string(8, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        if not Family.objects.filter(code=code).exists():
            return code


# ──────────────────────────────────────────────────────────
# ① 가족 생성용  (POST /families)
#    • 요청 : {"name":"우리집"}
#    • 응답 : {"code":"ABC12345"}
# ──────────────────────────────────────────────────────────
class FamilyCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, write_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Family
        fields = ('name', 'code', 'seeds')

    def create(self, validated_data):
        return Family.objects.create(code=_generate_code(), **validated_data)

    def to_representation(self, instance):
        # 응답은 코드만
        return {"code": instance.code}


# ──────────────────────────────────────────────────────────
# ② 가족 상세용  (GET /families/{code})
#    • 응답 : {"code":"ABC12345", "seeds":700}
# ──────────────────────────────────────────────────────────
class FamilyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ("code", "seeds")
        read_only_fields = fields

