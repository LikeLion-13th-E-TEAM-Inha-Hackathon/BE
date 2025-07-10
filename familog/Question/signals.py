from django.db.models.signals import post_migrate
from django.dispatch import receiver
from Question.models import QuestionPool

@receiver(post_migrate)
def insert_mock_questions(sender, **kwargs):
    if sender.name != "Question":
        return

    mock_questions = [
        "어린 시절 가장 좋아했던 장난감은 뭔가요?",
        "초등학교 혹은 중학교 때 가장 친했던 친구는 누구인가요?",
        "어릴 때 좋아했던 TV 프로그램은 뭔가요?",
        "가족 여행 중 가장 기억에 남는 여행지는 어디인가요?",
        "과거에 하지 못해서 미련이 남는 것은 무엇인가요?",
        "요즘 제일 자주 먹고 싶은 음식은?",
        "당신의 인생 식당을 자랑해주세요!",
        "가장 좋아하는 영화는 무엇인가요? 그 이유도 같이 말해주세요.",
        "자신만의 스트레스 풀이법을 알려주세요.",
        "지금 가장 배우고 싶은 것은 무엇인가요?",
        "로또 1등에 당첨된다면 제일 먼저 하고 싶은 건?",
        "우리 가족 중에서 가장 웃긴 사람은 누구인가요?",
        "부모님께 이 말만큼은 꼭 해주고 싶다!",
        "다른 가족들은 없을, 우리 가족만의 특별한 추억 한 가지를 떠올리면 무엇일까요?",
        "최근에 산 것 중에서 가장 만족스러운 물건은 무엇인가요?",
        "하루 중 가장 좋아하는 시간대는 언제인가요?",
        "무엇을 보면 부모님이 가장 먼저 떠오르나요?",
        "인생에서 가장 힘들었던 순간은 언제인가요?"
    ]

    existing = set(QuestionPool.objects.values_list("content", flat=True))
    to_create = [QuestionPool(content=q) for q in mock_questions if q not in existing]
    QuestionPool.objects.bulk_create(to_create)

    if to_create:
        print(f"📌 post_migrate: {len(to_create)}개 질문 자동 등록 완료")
