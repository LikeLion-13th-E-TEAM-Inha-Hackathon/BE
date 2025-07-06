from django.db import models


class Answer(models.Model):
    question = models.ForeignKey("Question.Question",
                                 on_delete=models.CASCADE,
                                 related_name="answers")
    member   = models.ForeignKey("FamilyMember.FamilyMember",
                                 on_delete=models.CASCADE,
                                 related_name="answers")
    content  = models.TextField()

    class Meta:
        unique_together = ("question", "member")

    def __str__(self):
        return f"{self.member.user.nickname}->{self.question.id}"
