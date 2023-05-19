from django.db import models
from commons.models import CommonModel


class Experience(CommonModel):
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    name = models.CharField(
        max_length=150
    )
    details = models.CharField(
        max_length=300,
        blank=True,
        null=True, # database 열에 빈값이 들어갈 수 있다.
    )
    explanation = models.TextField(
        blank=True,
        default="", # database 열에 ""란 값으로 들어간다.
    )

    def __str__(self):
        return self.name
