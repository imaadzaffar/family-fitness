from django.shortcuts import render, redirect
from .forms import FitnessRecordForm
from django.contrib.auth.decorators import login_required
from .models import UserLeaderboard, FitnessRecord

import datetime
from django.utils import timezone, dateparse
import sys

# Create your views here.
def home(request):
    context = {}
    return render(request, 'main/home.html', context)

def leaderboard(request):
    user_leaderboard_all = UserLeaderboard.objects.order_by('-total_calories')
    context = {
        'user_leaderboard_all': user_leaderboard_all
    }
    return render(request, 'main/leaderboard.html', context)

@login_required
def records(request):
    user = request.user
    records = FitnessRecord.objects.filter(user=user).order_by('-created')
    context = {
        'records': records
    }
    return render(request, 'main/records.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = FitnessRecordForm(request.POST)
        if form.is_valid():
            user = request.user
            category = request.POST.get('category')
            calories = int(request.POST.get('calories'))
            duration = request.POST.get('duration')
            duration = dateparse.parse_duration(duration)

            record = FitnessRecord(user=user, category=category, calories=calories, duration=duration)
            record.save()

            user_leaderboardeaderboard = UserLeaderboard.objects.filter(user=user).first()
            if user_leaderboardeaderboard is None:
                user_leaderboardeaderboard = UserLeaderboard()
                user_leaderboardeaderboard.user = user
                user_leaderboardeaderboard.total_calories = calories
                user_leaderboardeaderboard.total_duration = duration
            else:
                user_leaderboardeaderboard.total_calories += calories
                user_leaderboardeaderboard.total_duration += duration
                user_leaderboardeaderboard.updated = timezone.now()
            user_leaderboardeaderboard.save()

            return redirect('records')
    else:
        form = FitnessRecordForm()

    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)

@login_required
def edit(request, pk):
    if request.method == 'POST':
        record = FitnessRecord.objects.get(pk=pk)
        old_calories = record.calories
        old_duration = record.duration

        form = FitnessRecordForm(request.POST, instance=record)
        if form.is_valid():
            user = request.user
            category = request.POST.get('category')
            calories = int(request.POST.get('calories'))
            duration = request.POST.get('duration')
            duration = parse_duration(duration)

            difference_calories = calories - old_calories
            difference_duration = duration - old_duration

            record.category = category
            record.calories = calories
            record.duration = duration
            record.save()

            user_leaderboardeaderboard = UserLeaderboard.objects.get(user=user)
            user_leaderboardeaderboard.total_calories += difference_calories
            user_leaderboardeaderboard.total_duration += difference_duration
            user_leaderboardeaderboard.save()

            return redirect('records')
    else:
        record = FitnessRecord.objects.get(pk=pk)
        form = FitnessRecordForm(instance=record)

    context = {
        'form': form
    }
    return render(request, 'main/edit.html', context)

@login_required
def delete(request, pk):
    record = FitnessRecord.objects.get(pk=pk)
    calories = record.calories
    duration = record.duration
    record.delete()

    user_leaderboard = UserLeaderboard.objects.get(user=request.user)
    user_leaderboard.total_calories -= calories
    user_leaderboard.total_duration -= duration
    if user_leaderboard.total_calories == 0:
        user_leaderboard.delete()
    else:
        user_leaderboard.save()

    return redirect('records')
