# plant/views.py
"""
식물 · 물주기 API
─────────────────────────────────────────────────────────────
1. GET  /families/<code>/plant            ─ 화분 상태 조회
2. POST /families/<code>/plant/water      ─ 물 주기
"""

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from datetime import timedelta

from Family.models import Family
from FamilyMember.models import FamilyMember
from .models import Plant
from .serializers import (
    PlantDetailSerializer,
    PlantWaterResultSerializer,
)
from watering.models import Watering   # 물주기 이력 모델


# ──────────────────────────────────────────────────────────
# 공통 헬퍼
# ──────────────────────────────────────────────────────────
def _get_family(code: str) -> Family:
    return get_object_or_404(Family, code=code)


def _get_member(user, family: Family) -> FamilyMember:
    return get_object_or_404(FamilyMember, user=user, family=family)


# ──────────────────────────────────────────────────────────
# 1) 화분 상태  GET /families/<code>/plant
# ──────────────────────────────────────────────────────────
class PlantDetailView(generics.RetrieveAPIView):
    """
    응답 예: { "plantId":2, "growLevel":5, "lastWatered":"2025-07-04T12:00" }
    """
    serializer_class = PlantDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        family = _get_family(self.kwargs["code"])
        return family.plant  # One-to-One 관계


# ──────────────────────────────────────────────────────────
# 2) 물 주기  POST /families/<code>/plant/water
# ──────────────────────────────────────────────────────────
class PlantWaterView(generics.GenericAPIView):
    """
    요청 : {}   |   응답 : { "growLevel":6, "seeds":600 }
    - 씨앗 100개 이상 있어야 함
    - 마지막 물주기 후 최소 10초(예시) 지나야 다시 줄 수 있음
    """
    serializer_class = PlantWaterResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    SEEDS_PER_WATER = 100
    COOL_TIME = timedelta(seconds=10)   # 다시 물주기 제한 예시

    def post(self, request, *args, **kwargs):
        family = _get_family(self.kwargs["code"])
        member = _get_member(request.user, family)
        plant  = family.plant

        # cool-time 체크
        if plant.last_watered and (
            plant.last_watered + self.COOL_TIME > plant.last_watered.now()
        ):
            return Response(
                {"detail": "방금 물을 준 후 쿨타임입니다."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # 씨앗 체크
        if family.seeds < self.SEEDS_PER_WATER:
            return Response(
                {"detail": "씨앗이 부족합니다."},
                status=status.HTTP_409_CONFLICT,
            )

        # 트랜잭션으로 씨앗 차감 + 성장 단계 증가 + 로그생성
        with transaction.atomic():
            family.seeds -= self.SEEDS_PER_WATER
            family.save(update_fields=["seeds"])

            plant.grow_level += 1
            plant.last_watered = plant.last_watered.now()
            plant.save(update_fields=["grow_level", "last_watered"])

            Watering.objects.create(plant=plant, member=member)

        return Response(
            PlantWaterResultSerializer(plant).data,
            status=status.HTTP_201_CREATED,
        )
