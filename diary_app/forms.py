from django import forms
from tinymce.widgets import TinyMCE
from diary_app.models import Entry

class EntryForm(forms.ModelForm):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))
    content = forms.CharField(label="",widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Entry
        fields = ['title','content']
        exclude = ['entry_date']

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