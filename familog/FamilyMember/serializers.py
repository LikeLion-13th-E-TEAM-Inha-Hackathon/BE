# members/serializers.py
from rest_framework import serializers
from .models import FamilyMember


# ────────────────────────────────────────────────────────────
# ① 멤버 목록   GET /families/{code}/members
#    응답 예 : [{ "memberId":3, "nickname":"앨리스", "role":"MEMBER" }]
# ────────────────────────────────────────────────────────────
class FamilyMemberListSerializer(serializers.ModelSerializer):
    memberId = serializers.IntegerField(source="id", read_only=True)
    nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model  = FamilyMember
        fields = ("memberId", "nickname", "role")
        read_only_fields = fields


# ────────────────────────────────────────────────────────────
# ② 역할 변경   PATCH /families/{code}/members/{id}/role
#    요청 예 : { "role":"LEADER" }
# ────────────────────────────────────────────────────────────
class MemberRoleUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=FamilyMember.role_choices)

    class Meta:
        model  = FamilyMember
        fields = ("role",)
