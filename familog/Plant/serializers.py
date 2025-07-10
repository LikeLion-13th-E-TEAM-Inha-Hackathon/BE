# plant/serializers.py
from rest_framework import serializers
from .models import Plant


# ────────────────────────────────────────────────────────────
# ① 화분 상태  GET /families/{code}/plant
#    응답 예 : {
#      "plantId": 2,
#      "growLevel": 5,
#      "lastWatered": "2025-07-04T12:00",
#      "type": "sunflower"  ← ✅ 추가됨
#    }
# ────────────────────────────────────────────────────────────
class PlantDetailSerializer(serializers.ModelSerializer):
    plantId     = serializers.IntegerField(source="id", read_only=True)
    growLevel   = serializers.IntegerField(source="grow_level", read_only=True)
    lastWatered = serializers.DateTimeField(source="last_watered", read_only=True)
    type        = serializers.CharField(read_only=True)  # ✅ 추가된 필드

    class Meta:
        model  = Plant
        fields = ("plantId", "growLevel", "lastWatered", "type")  # ✅ type 포함
        read_only_fields = fields



# ────────────────────────────────────────────────────────────
# ② 물 주기 응답  POST /families/{code}/plant/water
#    응답 예 : { "growLevel":6, "seeds":600 }
# ────────────────────────────────────────────────────────────
class PlantWaterResultSerializer(serializers.ModelSerializer):
    growLevel = serializers.IntegerField(source="grow_level", read_only=True)
    seeds     = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Plant
        fields = ("growLevel", "seeds")

    def get_seeds(self, obj):
        # Plant ↔ Family 1:1 관계이므로 바로 참조
        return obj.family.seeds
