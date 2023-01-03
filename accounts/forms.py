from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from .models import MyUser
from django import forms
from django.contrib.auth.forms import SetPasswordForm

# user cre4ation form in django
class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'type':'password', 'align':'center', 'id':'password1' ,'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'type':'password', 'align':'center','id':'password2' , 'placeholder':'confirm password'}),
    )
    class Meta:
        model = MyUser
        fields = ['name','email','designation','password1','password2']
        widgets ={'name': forms.TextInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'First Name'}
            ),
            
            'email': forms.EmailInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'Email'}
            ),
            'designation': forms.TextInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'Designation'}
            ),
            

        }






# upate user profile form
class UpdateUserForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['email','name','designation','profile_pic']
        exclude = ('password',)
        widgets ={'name': forms.TextInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'First Name'}
            ),
            
            'email': forms.EmailInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'Email','id':"disabledTextInput",'readonly':True}
            ),
            'designation': forms.TextInput(
                attrs = {'class':'form-control form-control-lg','placeholder':'Designation'}
            ),
        }
# upate user profile form

class SetPasswordForm(SetPasswordForm):
    otp = forms.CharField(
        label="One time password",
        widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'type':'text', 'align':'center', 'placeholder':'Enter OTP'}),
    )
    new_password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'type':'password', 'align':'center', 'placeholder':'New Password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'type':'password', 'align':'center', 'placeholder':'confirm password'}),
    )
    class Meta:
        model = MyUser
        fields = ['new_password1', 'new_password2']
       