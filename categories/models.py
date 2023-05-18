from django.db import models
from commons.models import CommonModel

class Category(CommonModel):
    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=30,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"


