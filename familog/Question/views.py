from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Question, QuestionPool
from Family.models import Family
from django.utils.timezone import localdate
from django.shortcuts import get_object_or_404
import random

@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response("오늘의 질문")},
)
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

    return Response({
        "id": question.id,
        "date": str(question.q_date),
        "content": question.content,
        "is_completed": question.is_completed
    })


class QuestionView(APIView):
    @swagger_auto_schema(responses={200: openapi.Response("질문 서랍")})
    def get(self, request, code):
        family = get_object_or_404(Family, code=code)
        completed = request.GET.get("completed")

        questions = Question.objects.filter(family=family)
        if completed == "1":
            questions = questions.filter(is_completed=True)

        response = [
            {
                "id": q.id,
                "date": str(q.q_date),
                "is_completed": q.is_completed
            }
            for q in questions.order_by("-q_date")
        ]
        return Response(response)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["content"],
            properties={
                "content": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: openapi.Response("질문 추가")}
    )
    def post(self, request, code=None):  # code는 무시됨
        content = request.data.get("content")
        if not content:
            return Response({"message": "Invalid request"}, status=400)

        if QuestionPool.objects.filter(content=content).exists():
            return Response({"message": "이미 존재하는 질문입니다."}, status=400)

        q = QuestionPool.objects.create(content=content)
        return Response({"id": q.id})
