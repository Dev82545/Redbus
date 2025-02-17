# Generated by Django 5.1.5 on 2025-02-15 05:14

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='buses',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField(default='2025-01-01')),
                ('city1', models.CharField(max_length=255)),
                ('city2', models.CharField(max_length=255)),
                ('dep_time', models.CharField(max_length=255)),
                ('arr_time', models.CharField(max_length=255)),
                ('stops', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('is_booked', models.BooleanField(default=False)),
                ('luxury_seats', models.PositiveIntegerField(default=0)),
                ('sleeper_seats', models.PositiveIntegerField(default=0)),
                ('seats', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seat_booked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('lseat_number', models.IntegerField()),
                ('sseat_number', models.IntegerField()),
                ('buses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='redbus.buses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
