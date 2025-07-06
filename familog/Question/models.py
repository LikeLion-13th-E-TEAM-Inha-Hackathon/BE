from django.db import models
from django.utils import timezone


class Question(models.Model):
    family       = models.ForeignKey("Family.Family",
                                     on_delete=models.CASCADE,
                                     related_name="questions")
    q_date       = models.DateField(default=timezone.localdate)
    content      = models.TextField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("family", "q_date")

    def __str__(self):
        return f"Q-{self.family.code}-{self.q_date}"
