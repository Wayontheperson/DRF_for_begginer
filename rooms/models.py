from django.db import models
from commons.models import CommonModel


class Room(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room","Private Room")
        SHARED_ROOM = ("shared_room","Shared Room")

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
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms")

    def __str__(self):
        return self.name

    def total_amenities(self):
        print(dir(self.kind))
        return self.amenities.count()

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


