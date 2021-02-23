from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
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
