from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE

# Register your models here.

from .models import Entry
from .forms import EntryAdminForm



@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm