import datetime
from django.shortcuts import render
from diary_app.models import Entry

from diary_app.forms import EntryForm

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            print(form.get('content'))
            print(form.cleaned_data.get('content'))
            title = form.cleaned_data['title']
            content = form.cleaned_data.get('content')
            entry_date = datetime.date.today()
            # entry = Entry.objects.create(
            #     title=title,
            #     content=content,
            #     entry_date=entry_date,
            # )
    form = EntryForm()
    num_entries = Entry.objects.all().count()

    context = {
        'form': form,
        'num_entries': num_entries,
    }

    return render(request, 'index.html', context=context)