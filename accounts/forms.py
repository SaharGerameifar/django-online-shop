from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('پسوردها با هم مطابقت ندارند.')
        return cd['password2'] 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user 


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href=\"../password/\">تغییر پسورد</a>")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')    

messages = {
    'required': ' اين فيلد الزامي است.',
    'invalid': 'ايميل وارد شده معتبر نمی باشد.',
}
class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control input100'}),
           error_messages=messages
            )
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input100'}),
            validators=[validators.MaxLengthValidator(limit_value=40, message='نام و نام خانوادگی نمی تواند بیشتر از 40 کاراکتر باشد.') ], error_messages=messages
            )
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input100'}),
            validators=[
                validators.MaxLengthValidator(limit_value=11, message='شماره موبایل نمی تواند بیشتر از 11 کاراکتر باشد.'),
                validators.MinLengthValidator(11, 'شماره موبایل نمی تواند کمتر از 11 کاراکتر باشد.'),], error_messages=messages
        )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input100'}), error_messages=messages)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input100'}), error_messages=messages) 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری می باشد')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        is_exists_user_by_phone_number = User.objects.filter(phone_number=phone_number).exists()
        if is_exists_user_by_phone_number:
            raise forms.ValidationError('شماره موبایل وارد شده تکراری می باشد')
        return phone_number    

    def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 != password2:
                raise forms.ValidationError('پسوردها با هم مطابقت ندارند.')
            return password2


class UserVerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control input100'}), error_messages=messages)


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input100'}), error_messages=messages)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input100'}), error_messages=messages) 


class UserPasswordResetForm(PasswordResetForm ,forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control input100'}), error_messages=messages)


class UserSetPasswordForm(SetPasswordForm, forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input100'}), error_messages=messages)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input100'}), error_messages=messages) 

    def clean_password2(self):
            new_password1 = self.cleaned_data.get('new_password1')
            new_password2 = self.cleaned_data.get('new_password2')
            if new_password1 != new_password2:
                raise forms.ValidationError('پسوردها با هم مطابقت ندارند.')
            return new_password2

