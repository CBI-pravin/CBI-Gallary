from django.contrib import admin
from .models import mygallary,myfolder,myvideos

from rangefilter.filter import DateRangeFilter


# Register your models here.


def temp_delete_img(modeladmin, request, queryset):
    queryset.update(status=False)
temp_delete_img.short_description = "temporary delete post"



def restore_delete_img(modeladmin, request, queryset):
    queryset.update(status=True)
restore_delete_img.short_description = "restore deleted post"




def temp_delete_video(modeladmin, request, queryset):
    queryset.update(status=False)
temp_delete_img.short_description = "temporary delete video"



def restore_delete_video(modeladmin, request, queryset):
    queryset.update(status=True)
restore_delete_img.short_description = "restore deleted video"





# title for filter 
def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class PhotoAdmin(admin.ModelAdmin): # new
    readonly_fields = ['img_preview']
    list_display = ['owner', 'img_preview','status']
    list_filter = ['owner__designation',('status', custom_titled_filter('active post ')),('created_date',DateRangeFilter),'status']
    search_fields = ['owner__email','owner__name','owner__designation','description']
    list_per_page = 30
    actions = [temp_delete_img,restore_delete_img]
    ordering= ['-created_date']


class FolderAdmin(admin.ModelAdmin): # new
    fields = []
    readonly_fields = ['img_preview','folder_created_date',]
    list_display = ['name','folder_owner','folder_created_date']
     
    list_filter = [('folder_created_date',DateRangeFilter)]
    search_fields = ['name','folder_owner__name','folder_owner__email','folder_owner__designation']

    list_per_page = 30
    ordering= ['-folder_created_date']



class VideoAdmin(admin.ModelAdmin): # new
    fields = []
    readonly_fields = ['video_preview']
    list_display = ['video_owner','video_preview','video_created_date','status']
     
    list_filter = [('video_created_date',DateRangeFilter),'status']
    search_fields = ['video_owner__name','video_owner__email','video_owner__designation']

    list_per_page = 30
    ordering= ['-video_created_date']

    actions = [temp_delete_video,restore_delete_video]
  


  


    
   


admin.site.register(mygallary,PhotoAdmin)
admin.site.register(myfolder,FolderAdmin)
admin.site.register(myvideos,VideoAdmin)