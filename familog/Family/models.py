from django.db import models


class Family(models.Model):
    code  = models.CharField(max_length=8, primary_key=True)
    name  = models.CharField(max_length=30)
    seeds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
