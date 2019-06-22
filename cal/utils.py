from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from django.forms import ModelForm, DateInput
from django.utils.dateparse import parse_date

class Calendar(HTMLCalendar):
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
			if events_per_day.count() == 0:
				return f"<td><a class='date text-dark font-weight-bolder' href='/calendar/create/{self.year}/{self.month}/{day}/' data-year={self.year} data-month={self.month} data-day={day}>{day}</a><ul> {d} </ul></td>"
			else:
				return f"<td><a class='date text-dark font-weight-bolder' href='/calendar/create/{self.year}/{self.month}/{day}/' data-year={self.year} data-month={self.month} data-day={day}>{day}</a> <span class='date text-dark font-weight-bolder'>[{events_per_day.count()}]</span> <ul> {d} </ul></td>"
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

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
