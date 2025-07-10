from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Question, QuestionPool
from .serializers import QuestionSerializer, QuestionPoolCreateSerializer
from Family.models import Family
from django.utils.timezone import localdate
from django.shortcuts import get_object_or_404
import random


@swagger_auto_schema(method='get', responses={200: QuestionSerializer})
@api_view(["GET"])
def get_today_question(request, code):
    family = get_object_or_404(Family, code=code)
    today = localdate()

    question, created = Question.objects.get_or_create(
        family=family,
        q_date=today,
        defaults={"content": "", "is_completed": False}
    )

    if created:
        used_contents = Question.objects.filter(family=family).values_list("content", flat=True)
        candidates = QuestionPool.objects.exclude(content__in=used_contents)

        if not candidates.exists():
            return Response({ "message": "사용 가능한 질문이 없습니다." }, status=status.HTTP_404_NOT_FOUND)

        selected = random.choice(list(candidates))
        question.content = selected.content
        question.save()

    serializer = QuestionSerializer(question)
    return Response(serializer.data)


class QuestionView(APIView):
    @swagger_auto_schema(responses={200: QuestionSerializer(many=True)})
    def get(self, request, code):
        family = get_object_or_404(Family, code=code)
        completed = request.GET.get("completed")

        questions = Question.objects.filter(family=family)
        if completed == "1":
            questions = questions.filter(is_completed=True)

        serializer = QuestionSerializer(questions.order_by("-q_date"), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=QuestionPoolCreateSerializer,
        responses={200: openapi.Response("질문 추가 성공", QuestionPoolCreateSerializer)}
    )
    def post(self, request, code=None):
        serializer = QuestionPoolCreateSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response({"id": question.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
