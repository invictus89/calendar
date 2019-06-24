from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
from .models import *
from .utils import *
import calendar
from .forms import *
from django.urls import reverse
from pprint import pprint
from django.views.decorators.http import require_POST
from django.core import serializers
import json

def my_calendar(request, month = None):
    if month:
        year, month = (int(x) for x in month.split('-'))
        d = date(year, month, day=1)
    else:
        d = datetime.today()

    cal = Calendar(d.year, d.month)
    html_cal, month_name = cal.formatmonth(withyear=True)
    form = EventForm()
    context = {
        'form': form,
        'calendar': mark_safe(html_cal),
        'month_name': month_name,
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


def create(request, year, month, day):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        title_type = request.POST.get('title_type')
        
        temp = f'{year}-{month}-{day}'
        uploaded_at = datetime.strptime(temp, '%Y-%m-%d')
        event = Event(title = title, description = description, title_type = title_type, uploaded_at=uploaded_at)
        event.save()
    else:
        print("GET 방식의 HTTP 요청, POST 방식이여야 함")
    return redirect('calendar:calendar')

def detail(request, year, month, day):
    cur_temps = Event.objects.filter(uploaded_at__year=year, uploaded_at__month=month, uploaded_at__day=day)
    cur_dates = serializers.serialize('json', cur_temps)
    all_temps = Event.objects.filter(uploaded_at__month=month, uploaded_at__day=day)
    all_dates = serializers.serialize('json', all_temps)
    context = {
        'cur_dates': cur_dates,
        'all_dates': all_dates,
         }
    return JsonResponse(context)

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

'''
# modelForm 적용 create 
def create(request, year, month, day):
    if request.method == 'POST':
        print("포스트")
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
    context = {'form' : form,}
    return HttpResponse(context)
'''   