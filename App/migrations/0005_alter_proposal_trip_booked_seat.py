# Generated by Django 4.1.5 on 2023-01-30 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_location_take_trip_proposal_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal_trip',
            name='booked_seat',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
