from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.timezone import localdate
from .models import Question, QuestionPool
from Family.models import Family
from django.views import View
import json
import random

def get_today_question(request, code):
    family = get_object_or_404(Family, code=code)
    today = localdate()

    # 이미 오늘 질문이 있으면 반환
    question, created = Question.objects.get_or_create(
        family=family,
        q_date=today,
        defaults={"content": "", "is_completed": False}
    )

    if created:
        used_contents = Question.objects.filter(family=family).values_list("content", flat=True)
        candidates = QuestionPool.objects.exclude(content__in=used_contents)

        if not candidates.exists():
            return JsonResponse({ "message": "사용 가능한 질문이 없습니다." }, status=404)

        selected = random.choice(list(candidates))
        question.content = selected.content
        question.save()

    return JsonResponse({
        "id": question.id,
        "date": str(question.q_date),
        "content": question.content,
        "is_completed": question.is_completed
    })


class QuestionView(View):
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
        return JsonResponse(response, safe=False)

    def post(self, request, code=None):  # code는 무시됨
        try:
            data = json.loads(request.body)
            content = data["content"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({ "message": "Invalid request" }, status=400)

        if QuestionPool.objects.filter(content=content).exists():
            return JsonResponse({ "message": "이미 존재하는 질문입니다." }, status=400)

        q = QuestionPool.objects.create(content=content)
        return JsonResponse({ "id": q.id })