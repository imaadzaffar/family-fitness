from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
import uuid

# Create your models here.
class UserLeaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_calories = models.IntegerField(default=0)
    total_duration = models.DurationField(default=0)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}, {self.total_calories}'

class FitnessRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    class CategoryChoices(models.TextChoices):
        BIKE = 'Bike'
        WALK = 'Walk'
        RUN = 'Run'
        SPORTS = 'Sports'
     
    category = models.CharField(max_length=10, choices=CategoryChoices.choices, default=CategoryChoices.BIKE)

    calories = models.IntegerField(default=5)
    duration = models.DurationField(default='00:05:00', help_text='HH:MM:ss format')

    def __str__(self):
        return f'{self.user.username}, {self.category}, {self.calories}'
