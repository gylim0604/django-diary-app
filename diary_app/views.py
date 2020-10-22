import datetime
import calendar
import pytz

from django.shortcuts import render, redirect
from django.views import generic
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

#tinymce import
from tinymce.widgets import TinyMCE

# imports from this project
from diary_app.forms import EntryForm, EntryFormManual
from diary_app.models import *
from diary_app.utils import Calendar
import diary_app.services as service

@login_required
def index(request):
    # handle POST request
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('content'))
            title = form.cleaned_data['title']
            content = form.cleaned_data.get('content')
            
            #timezone to be stored in utc so should'nt change it here. instead should change when displaying
            entry_date = datetime.datetime.now(pytz.utc)
            entry = Entry.objects.create(
                title=title,
                content=content,
                entry_date=entry_date,
                author = request.user
            )
            entry.save()
            
    # this should be outside so a new form will always be created
    form = EntryForm()    
    num_entries = Entry.objects.all().count()

    context = {
        'form': form,
        'num_entries': num_entries,
        'quote': service.get_quote()
    }

    return render(request, 'index.html', context=context)

from django.contrib.auth.mixins import LoginRequiredMixin

# entry views
# list view filters entry on date and author
class EntryListView(LoginRequiredMixin,generic.ListView):
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        #should rename date to something else
        context['test'] = datetime.date.fromisoformat(self.kwargs['date'])
        return context

    def get_queryset(self):
        date = self.kwargs['date']
        #gets the date arguement, check if it exist, and filter the view if it exists
        if date != None:
            return Entry.objects.filter(author=self.request.user.id,entry_date__date = datetime.datetime.fromisoformat(date))
        else:
            return Entry.objects.all().order_by('-entry_date')[:10]

# need to take a date parameter to determine the date of the entry
class EntryCreateView(LoginRequiredMixin,generic.CreateView):
    model = Entry
    form_class = EntryFormManual
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        #should rename date to something else
        context['date'] = self.request.GET.get('date', None)
        return context

    def form_valid(self, form):
        article = form.save(commit=False)
        # get the date from the GET request and time from POST and combine into a datetime object
        date = datetime.datetime.strptime(self.request.GET.get('date',None),"%Y-%m-%d")
        time = datetime.datetime.strptime(form.clean_entry_time(), '%H:%M').time()
        article.entry_date = datetime.datetime.combine(date,time )
        # set the article author to current user
        article.author = self.request.user
        return super(EntryCreateView, self).form_valid(form)
   
class EntryDetailView(generic.DetailView):
    model = Entry

class EntryUpdateView(generic.UpdateView):
    model = Entry
    form_class = EntryForm
    template_name_suffix = '_update_form'

# calendar view
class CalendarView(LoginRequiredMixin,generic.ListView):
    model = Entry
    template_name = 'diary_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user,withyear=True)
        context['calendar'] = mark_safe(html_cal)


        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' +str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)

    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' +str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.date.today()

