# Generated by Django 4.2.5 on 2023-09-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooster_import', '0008_group_event_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='group',
        ),
        migrations.AddField(
            model_name='event',
            name='groups',
            field=models.ManyToManyField(to='rooster_import.group'),
        ),
    ]