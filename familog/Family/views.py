# families/views.py
"""
가족(Family) 관련 API 뷰 모음
─────────────────────────────────────────────────────────────
1. POST /families                ─ 가족 생성
2. GET  /families/<code>         ─ 가족 정보 조회
3. POST /families/<code>/join    ─ 가족 참여
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import Family
from .serializers import (
    FamilyCreateSerializer,
    FamilyDetailSerializer,
)
from FamilyMember.models import FamilyMember   # 멤버십 모델
from User.models import User                   # 인증 사용자 모델
from Plant.models import Plant  # 패밀리 생성 시 -> 해당 패밀리의 식물 자동 생성

# ────────────────────────────────────────────────────────────
# 1) 가족 생성  POST /families
# ────────────────────────────────────────────────────────────
class FamilyCreateView(generics.CreateAPIView):
    """
    요청  : {"name":"우리집"}
    응답  : {"code":"ABC12345"}
    """
    serializer_class = FamilyCreateSerializer
    permission_classes = [permissions.AllowAny]  # 회원가입 전에 가족 생성할 수도 있으므로
    
    def perform_create(self, serializer):
        family = serializer.save()

        # 1. 요청자가 로그인된 유저인 경우 => 방장으로 추가
        if self.request.user and self.request.user.is_authenticated:
            FamilyMember.objects.create(
                user=self.request.user,
                family=family,
                role=FamilyMember.LEADER
            )

        # 2. Plant 자동 생성
        Plant.objects.create(
        family=family,
        type="기본식물 🌱",        # ✅ 존재하는 필드
        grow_level=0,              # ✅ 기본값과 같지만 명시해도 OK
        last_watered=None          # ✅ or timezone.now()
    )

# ────────────────────────────────────────────────────────────
# 2) 가족 정보  GET /families/<code>
# ────────────────────────────────────────────────────────────
class FamilyDetailView(generics.RetrieveAPIView):
    """
    응답 : {"code":"ABC12345", "seeds":700}
    """
    queryset = Family.objects.all()
    serializer_class = FamilyDetailSerializer
    lookup_field = "code"
    permission_classes = [permissions.AllowAny]


# ────────────────────────────────────────────────────────────
# 3) 가족 참여  POST /families/<code>/join
# ────────────────────────────────────────────────────────────
class FamilyJoinView(generics.GenericAPIView):
    """
    요청 : {}
    응답 : {"memberId":3}
    """
    queryset = Family.objects.all()
    lookup_field = "code"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        family: Family = self.get_object()
        user: User = request.user
        
        # # [임시조치] 유저 하드코딩 or request에서 직접 가져오기
        # username = request.data.get("user")  # {"user": "rlawls1448"} 로 전달해줘야 함
        # try:
        #     user = User.objects.get(email=username)  # or nickname=username 등
        # except User.DoesNotExist:
        #     return Response({"detail": "사용자를 찾을 수 없습니다."}, status=400)
        # ####################

        # 이미 가족이 있는지(1유저 1가족 규칙) 검사
        if FamilyMember.objects.filter(user=user).exists():
            return Response(
                {"detail": "이미 다른 가족에 속해 있습니다."},
                status=status.HTTP_409_CONFLICT,
            )

        # 멤버십 생성 (기본 role=MEMBER)
        member = FamilyMember.objects.create(family=family, user=user)
        return Response({"memberId": member.id}, status=status.HTTP_201_CREATED)
