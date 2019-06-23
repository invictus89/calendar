from datetime import datetime, timedelta
from calendar import HTMLCalendar, TextCalendar
from .models import Event
from django.forms import ModelForm, DateInput
from django.utils.dateparse import parse_date
from pprint import pprint

class Calendar(TextCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(uploaded_at__day=day)
		d = ''
		limit_index = 3
		cur_index = 0
		if events_per_day.count() > limit_index:
			for event in events_per_day:
				d += f'<li> {event.get_html_url} </li>'
				cur_index += 1
				if cur_index > limit_index:
					break
			d += f'<li>...</li>'
		else:
			for event in events_per_day:
				d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			url = '/calendar/create/{self.year}/{self.month}/{day}/'
			a_class = 'date text-dark font-weight-bolder'
			date_cal = 'data-year={self.year} data-month={self.month} data-day={day}'
			if events_per_day.count() == 0:
				return f"<td><a class='{a_class}' {date_cal} data-toggle='modal' data-target='#myModal'>{day}</a><ul> {d} </ul></td>"
			else:
				return f"<td><a class='{a_class}' {date_cal} data-toggle='modal' data-target='#myModal'>{day}</a> <span class='date text-dark font-weight-bolder'>[{events_per_day.count()}]</span> <ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(uploaded_at__year=self.year, uploaded_at__month=self.month)
		month_name = self.formatmonthname(self.year, self.month, width=0, withyear=withyear)
		cal = ''
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal, month_name
