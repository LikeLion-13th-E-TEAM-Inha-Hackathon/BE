from django.db import models
from django.utils import timezone


class Watering(models.Model):
    plant  = models.ForeignKey("Plant.Plant",
                               on_delete=models.CASCADE,
                               related_name="waterings")
    member = models.ForeignKey("FamilyMember.FamilyMember",
                               on_delete=models.CASCADE,
                               related_name="waterings")
    time   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.member.user.nickname} watered {self.plant.family.code}"
