from django.db import models
from django.utils import timezone


class Plant(models.Model):
    family       = models.OneToOneField("Family.Family",
                                        on_delete=models.CASCADE,
                                        related_name="plant")
    type         = models.CharField(max_length=30)
    grow_level   = models.PositiveIntegerField(default=0)
    last_watered = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Plant-{self.family.code}"
