# Generated by Django 4.2.5 on 2023-09-12 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "rooster_import",
            "0007_remove_calendar_groups_calendar_courses_event_course_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
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
                ("name", models.CharField(max_length=255)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rooster_import.course",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="rooster_import.group",
            ),
        ),
    ]
