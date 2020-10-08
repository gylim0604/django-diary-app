from django import forms
from tinymce.widgets import TinyMCE

class EntryForm(forms.Form):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))
    content = forms.CharField(label="",widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    def clean_title(self):
        data = self.cleaned_data['title']
        return data
    
    def clean_content(self):
        data = self.cleaned_data['content']
        return data
