import datetime
from django.shortcuts import render
from diary_app.models import Entry
from django.views import generic
from django.views.generic.edit import UpdateView
from django.forms.models import modelform_factory
from tinymce.widgets import TinyMCE

from diary_app.forms import EntryForm

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
    else:
        form = EntryForm()
    
    num_entries = Entry.objects.all().count()

    context = {
        'form': form,
        'num_entries': num_entries,
    }

    return render(request, 'index.html', context=context)


class EntryListView(generic.ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.all()[:5]

class EntryDetailView(generic.DetailView):
    model = Entry

class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name_suffix = '_update_form'