# Generated by Django 4.1.6 on 2023-06-21 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0013_alter_booking_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeSlot',
            new_name='aTimeSlot',
        ),
    ]
