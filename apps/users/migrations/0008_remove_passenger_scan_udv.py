# Generated by Django 3.0.6 on 2022-06-01 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_passenger_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='scan_udv',
        ),
    ]