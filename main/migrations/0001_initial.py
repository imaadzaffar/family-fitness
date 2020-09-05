# Generated by Django 3.0.7 on 2020-09-05 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLeaderboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_calories', models.IntegerField(default=0)),
                ('total_duration', models.DurationField(default=0)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FitnessRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('Bike', 'Bike'), ('Walk', 'Walk'), ('Run', 'Run'), ('Sports', 'Sports')], default='Bike', max_length=10)),
                ('calories', models.IntegerField(default=5)),
                ('duration', models.DurationField(default='00:05:00', help_text='HH:MM:ss format')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
