from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect


from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import MyUser
from .forms import MyUserCreationForm, UpdateUserForm,SetPasswordForm
from django.http import Http404

import uuid
from django.urls import reverse

# send token to email function from utils .py file
from .utils import emailverificationfunction,emailverify_password_function

import random


# function to verify user with email and sended token to respective email
def verify_user(request):
    e=request.GET.get('e') if request.GET.get('e')!= None else False
    # q=request.GET.get('q') if request.GET.get('q')!= None else False
    if request.method == "POST":
    
        q=request.POST.get('otp')
        user = MyUser.objects.get(email = e)
        token = user.verify_token
        if token == q:
            user.is_active= True
            user.save()
            messages.success(request, 'Account verified successfully!' )
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong OTP. Check your email.' )
            return render(request,'accounts/verify_user.html',context={'email':e})

    else:
        messages.success(request, 'we have sent OTP to your email. Check your email.' )
        return render(request,'accounts/verify_user.html',context={'email':e})
   
            


def sign_up_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method== "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            obj=MyUser.objects.get(email = form.cleaned_data['email'])
            
            obj.verify_token = str(random.randrange(111111,999999,6))
            obj.is_active = False
            obj.save()
            # call verify function with token from atabase
            email_verify = emailverificationfunction(form.cleaned_data['email'],obj.verify_token)  
            if email_verify:
                email1 = form.cleaned_data['email']
               
                return HttpResponseRedirect(f'sign-up-user/verify-account/?e={email1}')  

            else:
                
                obj.delete()
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = MyUserCreationForm()
    context = {'form':form}
    return render(request,'accounts/sign_up_user.html',context)




def sign_in_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method== "POST":
        email1 = request.POST.get('email')
        password1 = request.POST.get('password')
        
        user = authenticate(request,email=email1, password=password1)
        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.error(request,'user name or password are not valid')
    
        
    context = {}
    return render(request,'accounts/sign_in_user.html',context)



def sign_out_user(request):
    logout(request)
    return render(request,'accounts/sign_in_user.html')



@login_required(login_url='sign_in_user')
def update_user(request,pk):
    """function to update user name email and profile pic """
    if request.user.id == pk:
        if request.method == "POST":
            form = UpdateUserForm(data=request.POST, files=request.FILES,instance = request.user)
            if form.is_valid():
                form.save()
                messages.success(request,'Account upated successfully!')
                id = request.user.id
                return HttpResponseRedirect(reverse('update_user', kwargs={'pk': id}))
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                id = request.user.id
                return HttpResponseRedirect(reverse('update_user', kwargs={'pk': id}))
        else:
            form = UpdateUserForm(instance=request.user)
            context = {'form' :form}
            return render(request, 'accounts/update_user.html',context)

    else:
        raise Http404




@login_required(login_url='sign_in_user')
def change_password(request,pk):

    """change password with otp verification """
    if request.user.id  == pk:
        try:
            obj = MyUser.objects.get(id =pk)
            user = request.user
        except Exception as E:
            raise Http404

        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                if otp == obj.verify_token:

                    form.save()
                    messages.success(request, "Your password has been changed.")
                    return redirect('sign_in_user')
                else:
                    messages.error(request,'you have enter wrong otp.')
                    return HttpResponseRedirect(reverse('change_password', kwargs={'pk': pk}))
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    
                return HttpResponseRedirect(reverse('change_password', kwargs={'pk': pk}))
        else:
            
            if obj:
                obj.verify_token = str(random.randrange(111111,999999,6))
                obj.save()

                email_verify = emailverify_password_function(obj.email,obj.verify_token) 
                if email_verify:
                    messages.success(request,'we have send OTP to your registered email to change your current password. please check your email.')
            form = SetPasswordForm(user)
            context = {'page': 'pass_otp','form':form}
            return render(request,'accounts/verify_user.html',context)
    else:
        raise Http404


def delete_acc(request,pk):

    """"deactivate user account from user side """
    if request.user.id == pk:
        if request.method == 'POST':
            email = request.user
            password = request.POST.get('password')
            user = authenticate(request,email=email, password=password)
            if user is not None:
                obj = MyUser.objects.get(id =pk)
                obj.is_active = False
                obj.save()
                return redirect('sign_in_user')
            else:
                messages.error(request,'Please enter valid password.')
                context = {'page': 'delete_acc'}
                return render(request,'accounts/verify_user.html',context)
        else:
            messages.success(request,"please enter your current password to delete your account.")
            context = {'page': 'delete_acc'}
            return render(request,'accounts/verify_user.html',context)
        
    else:
        raise Http404