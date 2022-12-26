from django.contrib import admin
from .models import MyUser

from rangefilter.filter import DateRangeFilter
# Register your models here.


def active_account(modeladmin, request, queryset):
    queryset.update(is_active=True)
active_account.short_description = "Activate user account"

def deactive_account(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactive_account.short_description = "Deactivate user account"

def make_superuser_account(modeladmin, request, queryset):
    queryset.update(is_superuser=True)
make_superuser_account.short_description = "make user account admin account"

def make_normal_account(modeladmin, request, queryset):
    queryset.update(is_superuser=False)
make_normal_account.short_description = "make admin account normal account"



class ProductAdmin(admin.ModelAdmin): # new
     readonly_fields = ['profile_picture_preview']
     list_display = ['name','email', 'designation','is_superuser','is_active','date_joined']
     # list_display = [field.name for field in MyUser._meta.fields if field.name != "user_permissions"]
     list_filter = [('date_joined',DateRangeFilter),'is_superuser','designation',]
     search_fields=['name','designation','email']
     actions = [active_account,deactive_account,make_superuser_account,make_normal_account]
     list_per_page = 30

     exclude = ['verify_token']


admin.site.register(MyUser,ProductAdmin)
