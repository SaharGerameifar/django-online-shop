from django.urls import path
from . import views


app_name = 'contacts'

urlpatterns = [
    path('', views.ContactUsView.as_view(), name='contact_us'),
]

