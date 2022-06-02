from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
from .models import ContactUs
from django.contrib import messages


class ContactUsView(View):
    template_name = 'contacts/contact.html'
    form_class = ContactForm

    def get(self, request):
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('body')
            ContactUs.objects.create(full_name=full_name, email=email, subject=subject, body=body, is_read=False)
            messages.success(request, 'پیام شما با موفقیت ثبت شد. به زودی بررسی خواهد شد.', 'success')
            return redirect('products:home')
        return render(request, self.template_name, {'form':form})
