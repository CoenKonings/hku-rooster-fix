# Generated by Django 4.2.5 on 2023-09-12 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rooster_import", "0006_calendar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="calendar",
            name="groups",
        ),
        migrations.AddField(
            model_name="calendar",
            name="courses",
            field=models.ManyToManyField(to="rooster_import.course"),
        ),
        migrations.AddField(
            model_name="event",
            name="course",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="rooster_import.course",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="calendarsource",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="track",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.DeleteModel(
            name="Group",
        ),
    ]
