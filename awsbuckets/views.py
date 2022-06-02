from django.shortcuts import render, redirect
from django.views import View
from . import tasks
from django.contrib import messages
from mixins import IsAdminUserMixin
from .forms import FileUploadForm


class AwsBucketList(IsAdminUserMixin, View):
    form_class = FileUploadForm
    template_name = 'awsbuckets/bucket_list.html'

    def get(self, request):
        form = self.form_class
        objects = tasks.all_bucket_objects_task()
        context = {
            'objects':objects,
            'form': form, 
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            key = form.cleaned_data['image']
            tasks.upload_object_task.delay(key)
            messages.success(request, 'به زودی آپلود خواهد شد.', 'info')
            return redirect('awsbuckets:list_bucket')
        messages.error(request, 'خطایی وجود دارد.', 'warning')
        return render(request, self.template_name, {'form':form})    


class AwsDeleteBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'به زودی حذف خواهد شد.', 'info')
        return redirect('awsbuckets:list_bucket')


class AwsDownloadBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'به زودی دانلود خواهد شد.', 'info')
        return redirect('awsbuckets:list_bucket')


  