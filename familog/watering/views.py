# watering/views.py
"""
물 주기 이력 API
─────────────────────────────────────────────────────────────
GET /families/<code>/watering/log
    └ 응답 예 :
      [
        { "time":"2025-07-04T12:00:00Z",
          "memberId":3,
          "nickname":"앨리스"
        },
        ...
      ]
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from Family.models import Family
from .models import Watering
from .serializers import WateringLogSerializer


class WateringLogListView(generics.ListAPIView):
    """
    • 가족 코드(<code>)로 해당 가족 Plant 의 물주기 이력을 반환
    • 최근 기록부터 역순 정렬
    """
    serializer_class = WateringLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # /families/<code>/watering/log 에서 <code> 추출
        family = get_object_or_404(Family, code=self.kwargs["code"])

        # Watering → Plant → Family  관계 (plant는 family와 1:1)
        return (
            Watering.objects
            .filter(plant__family=family)
            .select_related("member__user")      # nickname 가져오려면 조인
            .order_by("-time")                   # 최신순
        )
