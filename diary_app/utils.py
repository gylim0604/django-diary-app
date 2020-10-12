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
    def formatday(self, day, entries):
        entries_per_day = entries.filter(entry_date__day = day)
        d = ''
        for entry in entries_per_day:
            d += f'<li>{entry.title}</li>'
        
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    
    # format the week in a table row
    def formatweek(self, theweek, entries):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, entries)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear=True):
        entries = Entry.objects.filter(entry_date__year=self.year, entry_date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year,self.month):
            cal += f'{self.formatweek(week, entries)}\n'
        return cal