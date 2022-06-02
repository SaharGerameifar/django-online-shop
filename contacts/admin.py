from django.contrib import admin
from .models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'is_read', 'created')
    list_filter = (['is_read'])
    search_fields = (['full_name'])
    

