import datetime
from django.shortcuts import render
from django.views import generic
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.utils.safestring import mark_safe


#tinymce import
from tinymce.widgets import TinyMCE

# imports from this project
from diary_app.forms import EntryForm
from diary_app.models import *
from diary_app.utils import Calendar

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('content'))
            title = form.cleaned_data['title']
            content = form.cleaned_data.get('content')
            entry_date = datetime.date.today()
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

# entry views
class EntryListView(generic.ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.all()[:5]

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

        d = get_date(self.request.GET.get('day',None))

        cal = Calendar(d.year, d.month)

        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.date.today()