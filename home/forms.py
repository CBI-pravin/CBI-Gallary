from django.forms import ModelForm

from .models import mygallary,myvideos

from django import forms



class ImageUploadForm(ModelForm):
    

    class Meta:
        model = mygallary
        fields = ['image','description']
        widgets ={'image': forms.FileInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'Image','multiple': True,'id':"fileName", 'accept':".jpg,.jpeg,.png", 'onchange':"validateFileType()"}
            ),
            
            'description': forms.Textarea(
                attrs = {'class':'form-control form-control-lg','rows':'3','placeholder':'Description here .....'}
            ),
        }
class VideoUploadForm(ModelForm):
    

    class Meta:
        model = myvideos
        fields = ['video','video_description']
        widgets ={'video': forms.FileInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'Video File','multiple': True}
            ),
            
            'video_description': forms.Textarea(
                attrs = {'class':'form-control form-control-lg','rows':'3','placeholder':'Description here .....'}
            ),
        }











