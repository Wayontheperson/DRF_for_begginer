from django.db import models
from commons.models import CommonModel
from users.models import User


class Room(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=200,
        default="",
    )
    country = models.CharField(
        max_length=100,
        default="Korea",
    )
    city = models.CharField(
        max_length=200,
        default="Seoul",
    )

    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    descriptions = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(default=False)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
        default=1,
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms")
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):
    name = models.CharField(
        max_length=200,
    )
    descriptions = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
