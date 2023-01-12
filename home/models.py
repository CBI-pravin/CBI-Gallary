from django.db import models
from accounts.models import MyUser
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


from django.utils.html import mark_safe



# video file validator
from django.core.validators import FileExtensionValidator


# function to rename the uploaded images
@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        jpg = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = 'IMG{}.{}'.format(uuid4().hex, jpg)
        else:
            # set filename as random string
            filename = 'IMG{}.{}'.format(uuid4().hex, jpg)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)
@deconstructible
class UploadToPathAndRenameVideo(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        video = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = 'VIDEO{}.{}'.format(uuid4().hex, video)
        else:
            # set filename as random string
            filename = 'VIDEO{}.{}'.format(uuid4().hex, video)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)



# model class for ----- PHOTOS
class mygallary(models.Model):
    image = models.ImageField(upload_to=UploadToPathAndRename('media/'))
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    created_date =  models.DateTimeField(auto_now_add=True)

   
    status = models.BooleanField(default=True)

   
    def img_preview(self):
        """Method to return store image for admin panel"""  
        return mark_safe('<a href="{url}"/>{name}</a> <br><br> <img src = "{url}" height = "200"width = "300"/>'.format(
             url = self.image.url,name = self.image))        
         
    img_preview.allow_tags = True

    # def __str__(self) -> str:
    #     return mark_safe('<a href="{url}"/>{name}</a> <br><br> '.format(
    #          url = self.image.url,name = self.image))   




# model class for ----- FOLDER
class myfolder(models.Model):
    name= models.CharField(max_length=500)
    folder_owner = models.ForeignKey(MyUser,related_name='folder_owner',on_delete=models.CASCADE)
    photo = models.ManyToManyField(mygallary,related_name='photo',blank=True)
    folder_created_date  = models.DateTimeField(auto_now_add=True)
    

    # def img_preview(self): #new
    #     images = ''
    #     for img in self.photo.all():
    #         images += mark_safe('<img src = "{}" height = "300"width = "300"/>'.format(img.image.url))
    #         return images
    #     # img_preview.allow_tags = True

    # function to display image in admin pannel
    def img_preview(self):
        """Method to return store image for admin panel"""
        images = ''
        for image_path in self.photo.all():
            images+=('<img src = "{}" height = "150"width = "250"/> &nbsp <a href="%s"/>%s</a> &nbsp -> &nbsp %s <br><br> '.format(image_path.image.url) % (image_path.image.url,image_path,image_path.owner))   
        return mark_safe(images)         
         
    img_preview.allow_tags = True
    def __str__(self) -> str:
        return self.name




class myvideos(models.Model):
    video = models.FileField(upload_to=UploadToPathAndRenameVideo('media/video/'),validators=[FileExtensionValidator(allowed_extensions=["mp4",'mov','wmv','flv','avi','avchd ', "webm", "ogg"])])
    video_owner = models.ForeignKey(MyUser,related_name='video_owner',on_delete=models.CASCADE)
    video_description = models.TextField(null=True,blank=True)
    video_created_date  = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)



    

    def video_preview(self):
        """Method to return store image for admin panel"""  
        return mark_safe('<a href="{url}"/>{name}</a> <br><br> <video height = "200"width = "300" controls/> <source src="{url}"></video>'.format(
             url = self.video.url,name = self.video))          
         
    video_preview.allow_tags = True
    # def __str__(self) -> str:
    #     return self.name




    
          
