
# family_member/views.py
"""
가족 구성원(FamilyMember) API
─────────────────────────────────────────────────────────────
1. GET    /families/<code>/members                 ─ 멤버 목록
2. PATCH  /families/<code>/members/<id>/role       ─ 역할 변경
3. DELETE /families/<code>/members/<id>            ─ 추방 · 탈퇴
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from Family.models import Family          # 가족 모델
from .models import FamilyMember          # 멤버십 모델
from .serializers import (
    FamilyMemberListSerializer,
    MemberRoleUpdateSerializer,
)


# 공통 헬퍼 ────────────────────────────────────────────────
def _get_family(code: str) -> Family:
    """URL 파라미터 <code>로 Family 인스턴스 반환 (404 처리 O)"""
    return get_object_or_404(Family, code=code)


def _is_leader(user, family: Family) -> bool:
    """사용자가 해당 가족의 방장인지"""
    return FamilyMember.objects.filter(
        user=user, family=family, role=FamilyMember.LEADER
    ).exists()


# ─────────────────────────────────────────────────────────
# 1) 멤버 목록  GET /families/<code>/members
# ─────────────────────────────────────────────────────────
class MemberListView(generics.ListAPIView):
    """
    응답 :
    [
      { "memberId":3, "nickname":"앨리스", "role":"MEMBER" },
      ...
    ]
    """
    serializer_class = FamilyMemberListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        family = _get_family(self.kwargs["code"])
        return family.members.select_related("user").all()


# ─────────────────────────────────────────────────────────
# 2) 역할 변경  PATCH /families/<code>/members/<id>/role
# ─────────────────────────────────────────────────────────
class MemberRoleUpdateView(generics.UpdateAPIView):
    """
    요청 : { "role":"LEADER" }   | 응답 : 204 No Content
    - 방장만 수행 가능
    """
    serializer_class = MemberRoleUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "pk"           # 멤버 PK

    def get_queryset(self):
        family = _get_family(self.kwargs["code"])
        return FamilyMember.objects.filter(family=family)

    def update(self, request, *args, **kwargs):
        family = _get_family(self.kwargs["code"])

        # 방장 권한 체크
        if not _is_leader(request.user, family):
            return Response({"detail": "방장만 권한 변경 가능"},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


# ─────────────────────────────────────────────────────────
# 3) 추방·탈퇴  DELETE /families/<code>/members/<id>
# ─────────────────────────────────────────────────────────
class MemberDeleteView(generics.DestroyAPIView):
    """
    - 대상이 자기 자신 → 탈퇴
    - 요청자가 방장  → 추방
    응답 : 204 No Content
    - 추방 시 유저는 남고, 가족 멤버십만 삭제됨
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        family = _get_family(self.kwargs["code"])
        return FamilyMember.objects.filter(family=family)

    def destroy(self, request, *args, **kwargs):
        family = _get_family(self.kwargs["code"])
        target = self.get_object()

        # 1. 자기 자신 or 방장만 가능
        if target.user != request.user and not _is_leader(request.user, family):
            return Response({"detail": "권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        # 2. 멤버십만 삭제 (유저 계정은 유지)
        target.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
