# Generated by Django 5.1.5 on 2025-02-16 12:32

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redbus', '0005_seat_booked_final_available_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='buses',
            name='active_days',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=100, null=True),
        ),
    ]
