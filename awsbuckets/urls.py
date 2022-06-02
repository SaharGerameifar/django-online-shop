from django.urls import path, re_path
from . import views


app_name = 'awsbuckets'

urlpatterns = [
    path('', views.AwsBucketList.as_view(), name='list_bucket'),
    re_path(r'delete_obj/(?P<key>[^/]+)/', views.AwsDeleteBucketObject.as_view(), name='delete_obj_bucket'),
    re_path(r'download_obj/(?P<key>[^/]+)/', views.AwsDownloadBucketObject.as_view(), name='download_obj_bucket'),
     ]

