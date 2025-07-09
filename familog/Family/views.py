"""
가족(Family) 관련 API 뷰 모음
─────────────────────────────────────────────────────────────
1. POST /families                ─ 가족 생성
2. GET  /families/<code>         ─ 가족 정보 조회
3. POST /families/<code>/join    ─ 가족 참여
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Family
from .serializers import (
    FamilyCreateSerializer,
    FamilyDetailSerializer,
)
from FamilyMember.models import FamilyMember
from User.models import User
from Plant.models import Plant


# ────────────────────────────────────────────────────────────
# ✅ 가족 생성  POST /families
# ────────────────────────────────────────────────────────────
class FamilyCreateView(generics.CreateAPIView):
    """
    요청  : {"name":"우리집"}
    응답  : {"code":"ABC12345"}
    """
    serializer_class = FamilyCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        family = serializer.save()

        # 1. 요청자가 로그인된 유저인 경우 => 방장으로 추가
        if self.request.user and self.request.user.is_authenticated:
            FamilyMember.objects.create(
                user=self.request.user,
                family=family,
                role=FamilyMember.LEADER
            )

        # 2. 식물 자동 생성
        Plant.objects.create(
            family=family,
            type="기본식물 🌱",
            grow_level=0,
            last_watered=None
        )


# ────────────────────────────────────────────────────────────
# ✅ 가족 정보  GET /families/<code>
# ────────────────────────────────────────────────────────────
class FamilyDetailView(generics.RetrieveAPIView):
    """
    응답 : {"name": "상어가족", "code":"ABC12345", "seeds":700}
    """
    queryset = Family.objects.all()
    serializer_class = FamilyDetailSerializer
    lookup_field = "code"
    permission_classes = [permissions.AllowAny]


# ────────────────────────────────────────────────────────────
# ✅ 가족 참여 Serializer (요청/응답 명세용)
# ────────────────────────────────────────────────────────────
class FamilyJoinRequestSerializer(serializers.Serializer):
    """빈 요청용 — Swagger 문서 생성을 위해 명시"""
    pass


class FamilyJoinResponseSerializer(serializers.Serializer):
    memberId = serializers.IntegerField()


# ────────────────────────────────────────────────────────────
# ✅ 가족 참여  POST /families/<code>/join
# ────────────────────────────────────────────────────────────
class FamilyJoinView(generics.GenericAPIView):
    """
    요청 : {}
    응답 : {"memberId":3}
    """
    queryset = Family.objects.all()
    lookup_field = "code"
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FamilyJoinRequestSerializer  # Swagger용 빈 요청 스키마

    @swagger_auto_schema(
        request_body=FamilyJoinRequestSerializer,
        responses={201: FamilyJoinResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        # ✅ Swagger 요청 시 실행 방지
        if getattr(self, 'swagger_fake_view', False):
            return Response(status=200)

        family: Family = self.get_object()
        user: User = request.user

        # 이미 가족에 속해 있는지 검사
        if FamilyMember.objects.filter(user=user).exists():
            return Response(
                {"detail": "이미 다른 가족에 속해 있습니다."},
                status=status.HTTP_409_CONFLICT,
            )

        # 멤버십 생성
        member = FamilyMember.objects.create(family=family, user=user)
        return Response({"memberId": member.id}, status=status.HTTP_201_CREATED)
