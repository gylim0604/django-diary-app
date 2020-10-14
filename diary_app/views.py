import datetime
import calendar

from django.shortcuts import render, redirect
from django.views import generic
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


#tinymce import
from tinymce.widgets import TinyMCE

# imports from this project
from diary_app.forms import EntryForm
from diary_app.models import *
from diary_app.utils import Calendar


def index(request):
    # handle POST request
    if request.method == 'POST':
        form = EntryForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data.get('content'))
            title = form.cleaned_data['title']
            content = form.cleaned_data.get('content')
            #timezone to be stored in utc so should'nt change it here. instead should change when displaying
            entry_date = datetime.datetime.now()
            entry = Entry.objects.create(
                title=title,
                content=content,
                entry_date=entry_date,
            )
            entry.save()
            
    # this should be outside so a new form will always be created
    form = EntryForm()    
    num_entries = Entry.objects.all().count()

    context = {
        'form': form,
        'num_entries': num_entries,
    }

    return render(request, 'index.html', context=context)

def signup(request):
    #if user is signed in
    if request.user.is_authenticated:
        return redirect("/")
    # if is a post request
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # if valid form is provided
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #log user in and redirect to index
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'auth/signup.html', {'form':form})

# entry views
class EntryListView(generic.ListView):
    model = Entry

    def get_queryset(self):
        date = self.kwargs['date']
        #gets the date arguement, check if it exist, and filter the view if it exists
        if date != None:
            return Entry.objects.filter(entry_date__date = datetime.datetime.fromisoformat(date))
        else:
            return Entry.objects.all().order_by('-entry_date')[:10]

# class EntryListDateView(generic.ListView):
#     model = Entry

#     def get_queryset(self):
#         date = self.kwargs['date']
#         #gets the date arguement, check if it exist, and filter the view if it exists
#         if date != None:
#             return Entry.objects.filter(entry_date__date = datetime.datetime.fromisoformat(date))
#         else:
#             return Entry.objects.all().order_by('-entry_date')[:10]


class EntryCreateView(generic.CreateView):
    model = Entry
    form_class = EntryForm
    template_name_suffix = '_create_form'

        
class EntryDetailView(generic.DetailView):
    model = Entry

class EntryUpdateView(generic.UpdateView):
    model = Entry
    form_class = EntryForm
    template_name_suffix = '_update_form'

# calendar view
class CalendarView(generic.ListView):
    model = Entry
    template_name = 'diary_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
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