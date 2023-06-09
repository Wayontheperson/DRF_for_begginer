from django.db import models
from commons.models import CommonModel
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    experiences = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField(default=5,
                                         validators=[
                                             MaxValueValidator(5),
                                             MinValueValidator(1)
                                         ])

    def __str__(self):
        return f"{self.user} : {self.rating}"
