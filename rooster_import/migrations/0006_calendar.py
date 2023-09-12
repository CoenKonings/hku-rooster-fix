# Generated by Django 4.2.5 on 2023-09-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooster_import", "0005_rename_calendar_calendarsource"),
    ]

    operations = [
        migrations.CreateModel(
            name="Calendar",
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
                ("groups", models.ManyToManyField(to="rooster_import.group")),
                ("tracks", models.ManyToManyField(to="rooster_import.track")),
            ],
        ),
    ]
