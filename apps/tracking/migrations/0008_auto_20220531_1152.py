# Generated by Django 3.0.6 on 2022-05-31 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tracking", "0007_auto_20220530_2057"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="boardingpass",
            name="baggages",
        ),
        migrations.AddField(
            model_name="baggage",
            name="boarding",
            field=models.ForeignKey(
                default=8,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="baggages",
                to="tracking.BoardingPass",
            ),
            preserve_default=False,
        ),
    ]
