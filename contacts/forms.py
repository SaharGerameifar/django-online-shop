from django import forms
from .models import ContactUs
from django.core import validators
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input100'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control input100'}),
            validators=[validators.EmailValidator('ایمیل وارد شده معتبر نمی باشد')]
            )
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input100'}))        
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control input100', 'cols':'30', 'rows':'5' })) 
    captcha = ReCaptchaField(widget=ReCaptchaV3(
        attrs={
            'required_score':0.85,
            
        }))
