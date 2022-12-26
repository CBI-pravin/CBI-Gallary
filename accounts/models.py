from django.db import models
from django.contrib.auth.models import AbstractUser

import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


from django.utils.html import mark_safe


# function to change name of uploaded file and return whole path with image name
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


class MyUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    
    profile_pic = models.ImageField(upload_to=UploadToPathAndRename('media/profile pic/'),default='media/default_profile_picture.png')
    name = models.CharField(max_length=250)
    designation = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    verify_token = models.TextField(max_length=100,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','designation','username','profile_pic']
    
    # preview of image in admin pannel
    def profile_picture_preview(self): #new
        return mark_safe('<img src = "{url}" height = "300"width = "300"/>'.format(
             url = self.profile_pic.url))