from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Answer
from .serializers import AnswerCreateSerializer, AnswerListSerializer
from Family.models import Family
from Question.models import Question
from FamilyMember.models import FamilyMember


def get_family_member(user):
    return FamilyMember.objects.get(user=user)


class AnswerView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="답변 목록 조회",
        responses={200: AnswerListSerializer(many=True)}
    )
    def get(self, request, id):
        """답변 목록 조회"""
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        answers = Answer.objects.filter(question=question)
        serializer = AnswerListSerializer(answers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="답변 작성",
        request_body=AnswerCreateSerializer,
        responses={201: openapi.Response("답변 생성", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"answerId": openapi.Schema(type=openapi.TYPE_INTEGER)}
        ))}
    )
    def post(self, request, id):
        """답변 작성 (내 답변)"""
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        try:
            member = get_family_member(request.user)
        except FamilyMember.DoesNotExist:
            return Response({"error": "FamilyMember not found"}, status=404)

        # 🔒 이미 답변한 경우 중복 방지
        if Answer.objects.filter(question=question, member=member).exists():
            return Response({"error": "Answer already exists"}, status=400)

        serializer = AnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.save(member=member, question=question)

            # ✅ seeds +50
            family = question.family  # 더 명확하게 question에서 family 참조
            old_seeds = family.seeds
            family.seeds += 50
            family.save()
            print(f"[포인트] {family.name} ({family.code}): {old_seeds} → {family.seeds}")

            # ✅ 가족 구성원 답변 완료 여부 체크
            total_members = family.members.count()
            current_answer_count = Answer.objects.filter(question=question).count()
            if current_answer_count >= total_members:
                question.is_completed = True
                question.save()
                print("[완료] 모든 가족 구성원이 답변을 완료했습니다.")

            return Response({"answerId": answer.id}, status=201)

        return Response(serializer.errors, status=400)


class MyAnswerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="내 답변 수정",
        request_body=AnswerCreateSerializer,
        responses={204: "수정 완료", 404: "답변 없음"}
    )
    def patch(self, request, id):
        """내 답변 수정"""
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        member = get_family_member(request.user)

        try:
            answer = Answer.objects.get(question=question, member=member)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found"}, status=404)

        serializer = AnswerCreateSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)
