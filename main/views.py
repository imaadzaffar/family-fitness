import datetime
import sys

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.utils import dateparse, timezone

from .forms import FitnessRecordForm
from .models import FitnessRecord, UserLeaderboard


# Create your views here.
def home(request):
    context = {}
    return render(request, 'main/home.html', context)

def leaderboard(request):
    leaderboard_records = []

    for user_leaderboard in UserLeaderboard.objects.all():
        user = user_leaderboard.user
        user_records = FitnessRecord.objects.order_by('-created').filter(user=user, created__month=timezone.now().month)
        agg_stats = user_records.aggregate(total_calories=Coalesce(Sum('calories'), 0), total_duration=Coalesce(Sum('duration'), datetime.timedelta()))
        agg_stats['user'] = user
        agg_stats['last_record'] = user_records[0].created

        leaderboard_records.append(agg_stats)

    # Sort descending by calories
    leaderboard_records = sorted(leaderboard_records, key=lambda k: k['total_calories'], reverse=True)

    context = {
        'leaderboard_records': leaderboard_records
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
            duration = dateparse.parse_duration(request.POST.get('duration'))

            record = FitnessRecord(user=user, category=category, calories=calories, duration=duration)
            record.save()

            user_leaderboard = UserLeaderboard.objects.filter(user=user).first()
            if user_leaderboard is None:
                user_leaderboard = UserLeaderboard()
                user_leaderboard.user = user
                user_leaderboard.total_calories = calories
                user_leaderboard.total_duration = duration
            else:
                user_leaderboard.total_calories += calories
                user_leaderboard.total_duration += duration
                user_leaderboard.updated = timezone.now()
            user_leaderboard.save()

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
            duration = parse_duration(request.POST.get('duration'))

            difference_calories = calories - old_calories
            difference_duration = duration - old_duration

            record.category = category
            record.calories = calories
            record.duration = duration
            record.save()

            user_leaderboard = UserLeaderboard.objects.get(user=user)
            user_leaderboard.total_calories += difference_calories
            user_leaderboard.total_duration += difference_duration
            user_leaderboard.save()

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
