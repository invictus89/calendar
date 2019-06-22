from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
from .models import *
from .utils import *
import calendar
from .forms import *
from django.urls import reverse
from pprint import pprint

def calender(request, month = None):
    if month:
        year, month = (int(x) for x in month.split('-'))
        d = date(year, month, day=1)
    else:
        d = datetime.today()

    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)
    context = {
        'calendar': mark_safe(html_cal),
        'prev_month': prev_month(d),
        'next_month': next_month(d),
    }
    
    return render(request, 'cal/calendar.html', context)

def edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendar:calendar')
    else:
        form = EventForm(instance=event)
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'cal/form.html', context)

def create(request, year, month, day):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # 유저 기능 넣으면 해제 및 수정할 것
            # board = form.save(commit=False)
            # board.user = request.user
            temp = f'{year}-{month}-{day}'
            uploaded_at = datetime.strptime(temp, '%Y-%m-%d')
            event = form.save(commit=False)
            event.uploaded_at = uploaded_at
            event.save()
            return redirect('calendar:calendar')
    else:
        form = EventForm()
    context = {'form': form,}
    return render(request, 'cal/form.html', context)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = str(next_month.year) + '-' + str(next_month.month)
    return month