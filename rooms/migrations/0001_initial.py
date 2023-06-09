# Generated by Django 4.2.1 on 2023-05-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Amenity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200)),
                (
                    "descriptions",
                    models.CharField(blank=True, max_length=120, null=True),
                ),
            ],
            options={"verbose_name_plural": "Amenities",},
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(default="", max_length=200)),
                ("country", models.CharField(default="Korea", max_length=100)),
                ("city", models.CharField(default="Seoul", max_length=200)),
                ("price", models.PositiveIntegerField()),
                ("rooms", models.PositiveIntegerField()),
                ("toilets", models.PositiveIntegerField()),
                ("descriptions", models.TextField()),
                ("address", models.CharField(max_length=250)),
                ("pet_friendly", models.BooleanField(default=False)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("entire_place", "Entire Place"),
                            ("private_room", "Private Room"),
                            ("shared_room", "Shared Room"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
