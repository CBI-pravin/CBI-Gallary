from django.conf import settings
from django.core.mail import send_mail


# function to send verification code to email
def emailverificationfunction(email,token):
    try:
        subject = 'verification code'
        message = f'your otp for new registeration is :  {token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list ) 
        return True    
    except Exception as E:
        pass
def emailverify_password_function(email,otp):
    try:
        subject = 'verification code'
        message = f' your otp for change password is :  {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list ) 
        return True    
    except Exception as E:
        pass