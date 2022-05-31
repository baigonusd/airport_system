# Generated by Django 3.0.6 on 2022-05-30 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_passenger_photo'),
        ('tracking', '0006_auto_20220505_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='airline',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='from_location',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='time_finish',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='time_start',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='to_location',
        ),
        migrations.RemoveField(
            model_name='boardingpass',
            name='baggages',
        ),
        migrations.AddField(
            model_name='boardingpass',
            name='baggages',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='baggages', to='tracking.Baggage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='boardingpass',
            name='ticket',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='tracking.Ticket'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='users.Passenger'),
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('from_location', models.CharField(max_length=90, verbose_name='City/Country from')),
                ('to_location', models.CharField(max_length=90, verbose_name='City/Country to')),
                ('time_start', models.DateTimeField()),
                ('time_finish', models.DateTimeField()),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='tracking.Airline')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='boardingpass',
            name='flight',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='boarding', to='tracking.Flight'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='flight',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='tracking.Flight'),
            preserve_default=False,
        ),
    ]