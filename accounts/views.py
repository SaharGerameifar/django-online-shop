from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserVerifyCodeForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm
from random import randint
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from datetime import timedelta, datetime
import pytz
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from mixins import IsNotLoginUserMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        context = {
            'form': form, 
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registr_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password1'],
            }
            messages.success(request, 'یک کد فعال سازی برای حساب کاربری تان ارسال خواهد شد.', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form})


class UserRegisterVerifyCodeView( View):  
    form_class = UserVerifyCodeForm
    template_name = 'accounts/verify_code.html'

    def get(self, request):
        form = self.form_class
        context = {
            'form': form, 
        }
        return render(request, self.template_name, context) 

    def post(self, request): 
        form = self.form_class(request.POST)
        user_session = request.session['user_registr_info']  
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid(): 
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                expire_time_code = code_instance.created + timedelta(minutes=2)
                if expire_time_code > datetime.now(tz=pytz.timezone('Asia/Tehran')):
                    User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['full_name'], user_session['password'])
                    code_instance.delete()
                    messages.success(request, 'حساب کاربری شما با موفقیت فعال شد.', 'success')
                    return redirect('accounts:user_login')
                else:
                    messages.error(request, 'این کد فعال سازی منقضی شده است . لطفا دوباره ثبت نام کنید.', 'danger')
                    code_instance.delete()
                    return redirect('accounts:user_register')    
            else:
                messages.error(request, 'کد فعال سازی اشتباه است.', 'danger')
                return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form}) 


class UserLoginView( View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def get(self, request):
        form = self.form_class
        context = {
            'form': form, 
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'به پنل کاربری تان خوش آمدید.', 'info')
                return redirect('accounts:profile')
            messages.error(request, 'شماره موبایل یا ایمیل یا پسوردتان را اشتباه وارد کرده اید.', 'warning')
        return render(request, self.template_name, {'form':form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name, {})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت از سیستم خارج شدید.', 'success')
        return redirect('products:home')


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    # subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'accounts/password_reset_form.html'
    form_class = UserPasswordResetForm


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token' 


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    