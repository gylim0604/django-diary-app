from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE

# Register your models here.

from .models import Entry
from .forms import EntryAdminForm

class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = Entry
        widgets = {
            'content' : TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
        fields = '__all__'

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    # list_display = ('title', 'entry_date')
    # fields = [('title', 'entry_date'),'content']
    form = EntryAdminForm