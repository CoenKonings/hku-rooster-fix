# Generated by Django 4.2.5 on 2023-09-09 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooster_import', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
    ]
