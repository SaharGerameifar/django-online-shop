from django import forms


class FileUploadForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
