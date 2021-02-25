import datetime
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.utils import dateparse, timezone

from .forms import FamilyForm, FitnessRecordForm
from .models import Family, FitnessRecord


# Create your views here.
def home(request):
    user = request.user
    family = user.family_set.first()

    context = {
        'family': family,
    }
    return render(request, 'main/home.html', context)

def leaderboard(request):
    leaderboard_records = []

    users = User.objects.all()
    for user in users:
        user_records = FitnessRecord.objects.order_by('-created').filter(user=user)
        user_stats = user_records.filter(created__month=timezone.now().month).aggregate(total_calories=Coalesce(Sum('calories'), 0), total_duration=Sum('duration'))
        user_stats['user'] = user
        try:
            user_stats['last_record'] = user_records[0].created
        except:
            user_stats['last_record'] = None
        
        
        if (user_stats['total_duration'] is None):
            user_stats['total_duration'] = datetime.timedelta()

        leaderboard_records.append(user_stats)

    # Sort descending by calories
    leaderboard_records = sorted(leaderboard_records, key=lambda k: k['total_calories'], reverse=True)

    context = {
        'leaderboard_records': leaderboard_records
    }
    return render(request, 'main/leaderboard.html', context)

def create_family(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            user = request.user
            family = form.save(commit=False)
            family.save()
            family.members.add(user)
            form.save_m2m()

            return redirect('family_share')
    else:
        form = FamilyForm()

    context = {
        'form': form
    }
    return render(request, 'main/create_family.html', context)

def share_family(request):
    return redirect('home')

def join_family(request):
    return redirect('home')

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

    return redirect('records')
