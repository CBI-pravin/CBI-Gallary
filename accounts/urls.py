from django.urls import path
from .views import sign_up_user,sign_in_user,sign_out_user,update_user,verify_user,change_password,delete_acc



urlpatterns = [
    
    path('', sign_up_user,name='sign_up_user'),
    path('sign-in/', sign_in_user,name='sign_in_user'),
    path('sign-out/', sign_out_user,name='sign_out_user'),
    path('update-account/<int:pk>', update_user,name='update_user'),
    path('sign-up-user/verify-account/',verify_user,name='verify_user'),
    path('change_password/verify-account/<int:pk>/',change_password,name='change_password'),

    path('delete-account/<int:pk>/', delete_acc ,name='delete_acc')
    
]