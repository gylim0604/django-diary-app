from django.urls import reverse

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Entry

# This calendar was made based on https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats entries of a day into a table 
    def formatday(self, s, day, entries):
        entries_per_day = entries.filter(entry_date__day = day)[:2]
        d = ''
        for entry in entries_per_day:
            title = entry.title if len(entry.title) < 30 else entry.title[:27] + "..."
            d += f'<li>{title}</li>'

        # format string to contain leading zero if less than 2 digits   
        s += "-%02d" %(day)

        if day != 0:
            if s == datetime.today().strftime('%Y-%m-%d'):
                 return f'<td class="today"> <a href="{ reverse("entries", args={s}) } "> <span class="date">{day}</span> <ul> {d} </ul> </a> </td>'
            else:
                return f'<td> <a href="{ reverse("entries", args={s}) } "> <span class="date">{day}</span> <ul> {d} </ul> </a> </td>'
        return '<td></td>'
    
    # format the week in a table row
    def formatweek(self, s, theweek, entries):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(s,d, entries)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self,user, withyear=True):
        entries = Entry.objects.filter( author=user.id,entry_date__year=self.year, entry_date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year,self.month):
            s = str(self.year) + "-" + str(self.month)
            cal += f'{self.formatweek(s,week, entries)}\n'
        return cal