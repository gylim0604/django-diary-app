from django import forms
from tinymce.widgets import TinyMCE
from diary_app.models import Entry
from datetime import datetime

class EntryForm(forms.ModelForm):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))
    content = forms.CharField(label="",widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Entry
        fields = ['title','content']

    def clean_title(self):
        data = self.cleaned_data['title']
        return data
    
    def clean_content(self):
        data = self.cleaned_data['content']
        return data
    

from django.contrib.admin import widgets
# Need to modify so that it only takes the time, date will be merged 
class EntryFormManual(forms.ModelForm):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))
    content = forms.CharField(label="",widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    #NEED TO add the time field to the form
    # entry_time = forms.DateTimeField(widget= forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = Entry
        fields = ['title','content','entry_time']

    def clean_title(self):
        data = self.cleaned_data['title']
        return data
    
    def clean_content(self):
        data = self.cleaned_data['content']
        return data


class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = Entry
        widgets = {
            'content' : TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
        fields = '__all__'