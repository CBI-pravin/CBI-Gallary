from django.urls import path
from .views import  searchvideo,videoShow,home,upload_img,full_img,profile,deletePost,folder,remove_post_folder,add_img_folder,remove_img_folder,delete_folder,customFilter,searchfolder,upload_video
urlpatterns = [
    
    
    path('',home,name='home' ),
    path('videos/',videoShow,name='videos' ),
    path('filter/',customFilter,name='customFilter' ),

    path('folders/',folder,name='folder' ),
    path('folders/delete-folder/',delete_folder,name='delete_folder' ),

     path('folders/search/',searchfolder,name='searchfolder' ),
     path('videos/search/',searchvideo,name='searchvideo' ),


    path('folders/remove-post/',remove_post_folder,name='remove_post_folder'),
    path('folders/add-post/<int:pk>/',add_img_folder,name='add_img_folder'),
    path('folders/remove-post/<int:pk>/',remove_img_folder,name='remove_img_folder'),

    path('upload-img/',upload_img,name='upload_img' ),
    path('full-img/<int:pk>',full_img,name='full_img' ),
    path('delete-post/<int:pk>',deletePost,name='deletePost' ),



    path('upload-video/',upload_video,name='upload_video'),

    path('profile/<int:pk>/',profile,name='profile' ),
    
]