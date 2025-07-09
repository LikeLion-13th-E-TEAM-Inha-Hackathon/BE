
# User/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer
from FamilyMember.models import FamilyMember


class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer


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
            'nickname': user.nickname,
            'email': user.email,
            'code': code  # ✅ 추가
        })
        
# ✅ 회원 탈퇴
class UserDeleteView(generics.DestroyAPIView):
    """
    DELETE /users/<id>/  — 회원 탈퇴
    - 본인만 가능
    - 방장일 경우 다음 멤버에게 방장 위임
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "pk"

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # 본인만 탈퇴 가능
        if request.user != user:
            return Response({"detail": "본인만 탈퇴할 수 있습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        # 멤버십이 있다면
        member = FamilyMember.objects.filter(user=user).first()
        if member:
            family = member.family

            if member.role == FamilyMember.LEADER:
                # 다음 멤버에게 방장 위임
                next_member = FamilyMember.objects.filter(
                    family=family
                ).exclude(user=user).order_by("id").first()

                if next_member:
                    next_member.role = FamilyMember.LEADER
                    next_member.save(update_fields=["role"])

            # 멤버십 삭제
            member.delete()

        # 유저 계정 삭제
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
