from django import forms
from django.core import validators


class CartAddForm(forms.Form):
        quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control d-inline w-25'}),
            min_value=1, max_value=3
    )


class CouponApplyForm(forms.Form):
        code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control d-inline w-50', 'placeholder':'لطفا كد تخفیف خود را وارد كنيد'})) 


class CheckOutForm(forms.Form):
        address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'لطفا آدرس خود را وارد كنيد', 'cols':'30', 'rows':'3' }))
        post_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'لطفا كد پستي خود را وارد كنيد'}),
           validators=[
                validators.MaxLengthValidator(limit_value=16, message='کد پستی نمی تواند بیشتر از 16 کاراکتر باشد'),]
                        )
