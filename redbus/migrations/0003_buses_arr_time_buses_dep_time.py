# Generated by Django 5.1.5 on 2025-02-09 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redbus', '0002_buses_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='buses',
            name='arr_time',
            field=models.CharField(default='9:45', max_length=255),
        ),
        migrations.AddField(
            model_name='buses',
            name='dep_time',
            field=models.CharField(default='4:30', max_length=255),
        ),
    ]
