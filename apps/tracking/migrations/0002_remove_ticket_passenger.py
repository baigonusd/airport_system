# Generated by Django 3.0.6 on 2022-04-30 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='passenger',
        ),
    ]