# Generated by Django 5.1.5 on 2025-02-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redbus', '0005_alter_buses_arr_time_alter_buses_dep_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buses',
            name='seats',
            field=models.IntegerField(max_length=255),
        ),
    ]
