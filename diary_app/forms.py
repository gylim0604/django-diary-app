from django import forms

class EntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.Textarea()
    
    def clean_title(self):
        data = self.cleaned_data['title']
        return data
    
    def clean_content(self):
        data = self.cleaned_data['content']
        return data
