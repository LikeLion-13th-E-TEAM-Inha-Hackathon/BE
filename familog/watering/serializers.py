# watering/serializers.py
from rest_framework import serializers
from .models import Watering


# ────────────────────────────────────────────────────────────
# 물 주기 이력  GET /families/{code}/watering/log
# 응답 예 : [ { "time":"2025-07-04T12:00", "memberId":3, "nickname":"앨리스" } ]
# ────────────────────────────────────────────────────────────
class WateringLogSerializer(serializers.ModelSerializer):
    memberId = serializers.IntegerField(source="member.id", read_only=True)
    nickname = serializers.CharField(source="member.user.nickname", read_only=True)

    class Meta:
        model  = Watering
        fields = ("time", "memberId", "nickname")
        read_only_fields = fields
