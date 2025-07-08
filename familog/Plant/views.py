from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

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


def calc_grow_level(watering_count: int) -> int:
    """물 준 횟수에 따라 성장 단계 계산 (초기 빠르고 후반 느림)"""
    if watering_count < 5:
        return 0
    elif watering_count < 15:
        return 1
    elif watering_count < 30:
        return 2
    else:
        return 3


# ──────────────────────────────────────────────────────────
# 1) 화분 상태  GET /families/<code>/plant
# ──────────────────────────────────────────────────────────
class PlantDetailView(generics.RetrieveAPIView):
    """
    응답 예: { "plantId":2, "growLevel":2, "wateringCount":17 }
    """
    serializer_class = PlantDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        family = _get_family(self.kwargs["code"])
        return family.plant


# ──────────────────────────────────────────────────────────
# 2) 물 주기  POST /families/<code>/plant/water
# ──────────────────────────────────────────────────────────
class PlantWaterView(generics.GenericAPIView):
    """
    요청 : {}   |   응답 : { "growLevel":2, "seeds":600 }

    - 씨앗 100개 이상 있어야 함
    - 물 줄 때마다 watering_count +1, grow_level 재계산
    """
    serializer_class = PlantWaterResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    SEEDS_PER_WATER = 100

    def post(self, request, *args, **kwargs):
        family = _get_family(self.kwargs["code"])
        member = _get_member(request.user, family)
        plant = family.plant

        # 씨앗 부족 체크
        if family.seeds < self.SEEDS_PER_WATER:
            return Response(
                {"detail": "씨앗이 부족합니다."},
                status=status.HTTP_409_CONFLICT,
            )

        # 트랜잭션 처리
        with transaction.atomic():
            family.seeds -= self.SEEDS_PER_WATER
            family.save(update_fields=["seeds"])

            plant.watering_count += 1
            plant.grow_level = calc_grow_level(plant.watering_count)
            plant.save(update_fields=["watering_count", "grow_level"])

            Watering.objects.create(plant=plant, member=member)

        return Response(
            PlantWaterResultSerializer(plant).data,
            status=status.HTTP_201_CREATED,
        )
