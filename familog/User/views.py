from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer
from FamilyMember.models import FamilyMember


# ─────────────────────────────────────────────
# 회원가입
# ─────────────────────────────────────────────
class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer


# ─────────────────────────────────────────────
# 로그인
# ─────────────────────────────────────────────
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        # 가족 코드 가져오기
        code = None
        member = FamilyMember.objects.filter(user=user).first()
        if member:
            code = member.family.code

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'userId': user.id,
            'nickname': user.nickname,
            'email': user.email,
            'code': code
        })


# ─────────────────────────────────────────────
# 회원 탈퇴
# ─────────────────────────────────────────────
class UserDeleteView(generics.DestroyAPIView):
    """
    DELETE /users/<id>/ — 회원 탈퇴
    - 본인만 가능
    - 방장일 경우 다음 멤버에게 방장 위임
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "pk"

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        if request.user != user:
            return Response({"detail": "본인만 탈퇴할 수 있습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        member = FamilyMember.objects.filter(user=user).first()
        if member:
            family = member.family

            if member.role == FamilyMember.LEADER:
                next_member = FamilyMember.objects.filter(
                    family=family
                ).exclude(user=user).order_by("id").first()

                if next_member:
                    next_member.role = FamilyMember.LEADER
                    next_member.save(update_fields=["role"])

            member.delete()

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────
# 사용자 상세 조회 (프론트 fetchUserInfo용)
# ─────────────────────────────────────────────
class UserDetailView(APIView):
    """
    GET /users/<id>/ — 사용자 정보 + 가족 구성원 + 가족 코드 반환
    - 누구나 조회 가능
    """
    permission_classes = [AllowAny]  # ✅ 누구나 접근 가능

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        user_info = {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname
        }

        member = FamilyMember.objects.filter(user=user).first()
        if not member:
            return Response({
                "user": user_info,
                "members": [],
                "familyCode": None
            })

        family_members = FamilyMember.objects.filter(family=member.family).select_related("user")
        members_data = [
            {
                "memberId": m.id,
                "nickname": m.user.nickname,
                "role": m.role
            }
            for m in family_members
        ]

        return Response({
            "user": user_info,
            "members": members_data,
            "familyCode": member.family.code
        })
