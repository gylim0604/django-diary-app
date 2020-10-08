from django.contrib import admin

# Register your models here.

from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'entry_date')
    fields = [('title', 'entry_date'),'content']