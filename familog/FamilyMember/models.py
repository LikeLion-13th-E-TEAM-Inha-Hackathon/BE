from django.db import models


class FamilyMember(models.Model):
    LEADER = "LEADER"
    MEMBER = "MEMBER"
    role_choices = [(LEADER, "Leader"), (MEMBER, "Member")]

    family = models.ForeignKey("Family.Family",
                               on_delete=models.CASCADE,
                               related_name="members")
    user   = models.ForeignKey("User.User",
                               on_delete=models.CASCADE,
                               related_name="memberships")
    role   = models.CharField(max_length=6, choices=role_choices,
                              default=MEMBER)

    class Meta:
        unique_together = ("family", "user")

    def __str__(self):
        return f"{self.user.nickname}@{self.family.code}"
