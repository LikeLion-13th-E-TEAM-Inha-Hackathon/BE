from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Answer
from .serializers import AnswerCreateSerializer, AnswerListSerializer
from Question.models import Question
from FamilyMember.models import FamilyMember


def get_family_member(user):
    return FamilyMember.objects.get(user=user)


class AnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """답변 목록 조회"""
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        answers = Answer.objects.filter(question=question)
        serializer = AnswerListSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        """답변 작성 (내 답변)"""
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        member = get_family_member(request.user)

        if Answer.objects.filter(question=question, member=member).exists():
            return Response({"error": "Answer already exists"}, status=400)

        serializer = AnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.save(member=member, question=question)
            return Response({"answerId": answer.id}, status=201)
        return Response(serializer.errors, status=400)


class MyAnswerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

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
