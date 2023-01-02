from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse

from django.contrib.auth.decorators import login_required




from .forms import ImageUploadForm,VideoUploadForm
from .models import mygallary,MyUser,myfolder,myvideos

from django.core.paginator import Paginator


from django.db.models import Q



def error_500(request):
    return render(request, '500.html')


@login_required(login_url='sign_in_user')
def searchfolder(request):
    q = request.GET.get('search') if request.GET.get('search')!= None else ''
    
    folder = myfolder.objects.filter(Q(name__icontains=q)|Q (folder_owner__name__icontains=q) ).order_by('-folder_created_date')
   
    if folder:
        context = {'obj':folder}
    
        return render(request,'home/folder.html' ,context)
    else:
        messages.error(request,'no result found.')
        return redirect('folder')


@login_required(login_url='sign_in_user')
def searchvideo(request):
    q = request.GET.get('search') if request.GET.get('search')!= None else ''
    
    folder = myvideos.objects.filter(Q(video_description__icontains=q)|Q (video_owner__name__icontains=q),status = True).order_by('-video_created_date')
   
    if folder:
        context = {'videos':folder}
    
        return render(request,'home/videos.html' ,context)
    else:
        messages.error(request,'no result found.')
        return redirect('videos')



# function to filter out images with giver parameters
@login_required(login_url='sign_in_user')
def customFilter(request):
    if request.method == "POST":
        std = request.POST.get('strtDT') if request.POST.get('strtDT')!= '' else False
        enddt = request.POST.get('endDT') if request.POST.get('endDT')!= '' else False
       
        print(enddt)
        if std or enddt :

            if enddt and  std :
                obj = mygallary.objects.filter(created_date__range = (std, enddt) ,status = True).order_by('-created_date')
                
                context= {'image':obj}
                return render(request,'home/index3.html',context)

            elif enddt:
                obj = mygallary.objects.filter(created_date__lte = enddt ,status = True).order_by('-created_date')
                
                context={'image':obj}
                return render(request,'home/index3.html',context)
            elif std:
                obj = mygallary.objects.filter(created_date__gte  =std,status = True).order_by('-created_date')
                
                context={'image':obj}
                return render(request,'home/index3.html',context)
        else:
            messages.error(request,'please select valid filter')
       
            return redirect('home')




@login_required(login_url='sign_in_user')
def home(request):
    posts = mygallary.objects.filter(status = True).order_by('-created_date')
    p = Paginator(posts, 28)
    page_number = request.GET.get('page') if request.GET.get('page')!= None else 1
    try:
        page_obj = p.get_page(page_number) 
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    # page_no = p.get_elided_page_range(number=page_number)
    page_obj.adjusted_elided_pages = p.get_elided_page_range(page_number)
    context ={'page_obj': page_obj,'image':page_obj}
    return render(request,'home/index3.html',context)


@login_required(login_url='sign_in_user')
def videoShow(request):
    posts = myvideos.objects.filter(status = True).order_by('-video_created_date')
    p = Paginator(posts, 16)
    page_number = request.GET.get('page') if request.GET.get('page')!= None else 1
    try:
        page_obj = p.get_page(page_number) 
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    page_obj.adjusted_elided_pages = p.get_elided_page_range(page_number)
    context ={'page_obj': page_obj,'videos':page_obj}
    # return render(request,'home/index3.html',context)
    return render(request,'home/videos.html',context)

   



@login_required(login_url='sign_in_user')
def upload_img(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ImageUploadForm(data=request.POST, files=request.FILES)
            var=request.FILES.getlist('image')
            pk= request.user.id
            if form.is_valid():
                bulk_list = []
                for img in var:
                    bulk_list.append(mygallary(image=img, owner= MyUser.objects.get(id=pk),description=form.cleaned_data['description']))
                try:
                    mygallary.objects.bulk_create(bulk_list)
                    messages.success(request,"image uploaded successfully")
                    form = ImageUploadForm()
                except Exception as E:
                    raise HttpResponse(status=500)
               
            else:
                messages.error(request,'{}'.format(form.errors))            
        else:
            form = ImageUploadForm()

        context = {'form':form}

        return render(request,'home/upload_img.html',context)
    else:
        raise Http404


@login_required(login_url='sign_in_user')
def upload_video(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = VideoUploadForm(data=request.POST, files=request.FILES)
          
            if form.is_valid():
                try:
                    form = form.save(commit=False)
                    form.video_owner = request.user
                    form.save()
                    messages.success(request,"video uploaded successfully")
                    form = VideoUploadForm()
                except Exception as E:
                    raise HttpResponse(status=500)
            else:
                messages.error(request,'{}'.format(form.errors))            
        else:
            form = VideoUploadForm()

        context = {'form':form,'page':'video_upload'}

        return render(request,'home/upload_img.html',context)
    else:
        raise Http404



@login_required(login_url='sign_in_user')
def full_img(request,pk):
    try:
        obj = mygallary.objects.get(id=pk,status = True)
        context = {'image': obj}
        return render(request,'home/full_img.html',context)
    except Exception as E:
        raise Http404
    






@login_required(login_url='sign_in_user')
def profile(request,pk):
    try:
        user = MyUser.objects.get(id =pk)
        img = mygallary.objects.filter(owner=pk,status = True).order_by('-created_date')
        context = {'obj': user,'img':img}
        return render(request,'home/profile.html',context)
    except Exception as E:
        raise Http404
    
   


@login_required(login_url='sign_in_user')
def deletePost(request,pk): 
    """function to delete post from user and super user"""
    var = request.user.is_superuser
    obj = mygallary.objects.get(id = pk,status = True)
    owner_is = obj.owner
    if var or request.user == owner_is: 
        try:
            obj.status = False
            obj.save()
            return redirect('home')
        except Exception as E:
            raise HttpResponse(status=500)
    else:
        raise Http404




# ------------function for folder pagination -----------------------------------------
def folder_pafination(request):
    posts = myfolder.objects.all().order_by('-folder_created_date')# fetching all post objects from database
    p = Paginator(posts, 24)
    page_number = request.GET.get('page') if request.GET.get('page')!= None else 1
    try:
        page_obj = p.get_page(page_number) 
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    page_obj.adjusted_elided_pages = p.get_elided_page_range(page_number)
    context = {'page_obj': page_obj,'obj':page_obj}
    return context 
# ------------ end function for folder pagination -----------------------------------------






@login_required(login_url='sign_in_user')
def folder(request):
    # super user
    super_user = request.user.is_superuser

    # __________query set to fetch all photos from a folder_________
    q = request.GET.get('q') if request.GET.get('q')!= None else False
    if q :
        try:
            folder = myfolder.objects.get(id = q)
            context = { 'folder':folder}
            return render(request,'home/folder_photos.html' ,context)
        except Exception as E:
            raise Http404

      
    # _______________new folder creation code____________
    folder_name = request.GET.get('folder_name') if request.GET.get('folder_name')!= None else False
    if folder_name:
        if super_user:
            try:
                obj = myfolder.objects.create(name=folder_name, folder_owner = request.user )
                obj.save()
                return redirect('folder')
            except Exception as E:
                raise HttpResponse(status=500)

    # default query to load folders from database
    context = folder_pafination(request)
    
	# sending the page object to index.html
    return render(request,'home/folder.html' ,context)





@login_required(login_url='sign_in_user')
def remove_post_folder(request):
    """ function for removing single post from folder with image id and folder id"""
    super_user = request.user.is_superuser
    
    i = request.GET.get('i') if request.GET.get('i')!= None else False
    f= request.GET.get('f') if request.GET.get('f')!= None else False
    
    if i and f and super_user:
        try:
            folder = myfolder.objects.get(id = f)
            folder.photo.remove(mygallary.objects.get(id=i))
            folder.save()
            return HttpResponseRedirect(f'/home/folders/?q={f}')

        except Exception as e:
            raise HttpResponse(status=500)
    else:
        raise Http404


@login_required(login_url='sign_in_user')   
def add_img_folder(request,pk):
    """ function to add multiple photos in folder"""
    if request.user.is_superuser:
    # method to get list of photos and save to folder
        if request.method == "POST":
            super_user = request.user.is_superuser
            if super_user:           
                var= request.POST.getlist('imagesID')
                if var:
                    folder = myfolder.objects.get(id = pk)
                    for i in var:
                        folder.photo.add(mygallary.objects.get(id=i))
        
            
            return HttpResponseRedirect(f'/home/folders/?q={pk}')
        

        else:

            # code to fetch all image from gallary where image not present in folder
            try:
            
                obj = mygallary.objects.raw(f"SELECT * FROM home_mygallary where id not in (SELECT mygallary_id FROM cbigallary.home_myfolder_photo where myfolder_id ={pk}) AND status = True ORDER BY created_date DESC ")
                
                foldername = myfolder.objects.get(id=pk).name

                context = {'image':obj,'folder':pk,'folder_name':foldername}
            
                return render(request,'home/add_img_folder.html',context)
            except Exception as E:
                raise HttpResponse(status=500)
    else:
        raise Http404      





@login_required(login_url='sign_in_user')
def remove_img_folder(request,pk):
    """ function to remove multiple photos multiple photo"""
    if request.user.is_superuser:
        if request.method == "POST":
            var= request.POST.getlist('imagesID')
            super_user = request.user.is_superuser
            if super_user:
                if var:
                    folder = myfolder.objects.get(id = pk)
                    for i in var:
                        folder.photo.remove(mygallary.objects.get(id=i))
            
            
            return HttpResponseRedirect(f'/home/folders/?q={pk}')
        else:
            try:
                foldername = myfolder.objects.get(id=pk)
                context = {'folder':foldername}
                return render(request,'home/remove_img_folder.html',context)
            except Exception as E:
                raise Http404
    else:
        raise Http404



#  ______delete multiple folder_____________________
@login_required(login_url='sign_in_user')
def delete_folder(request):
    if request.user.is_superuser:
        if request.method == "POST":
            super_user = request.user.is_superuser
            var= request.POST.getlist('checkboxCBI')
            if super_user:
                if var:
                    for i in var:
                        folder = myfolder.objects.get(id = i)
                        folder.delete()
                return redirect('folder')

        else:
            try:
                obj = myfolder.objects.all().order_by('-folder_created_date')
                context = {'obj': obj}
                return render(request,'home/delete_folder.html' ,context)  
            except Exception as E:
                raise HttpResponse(status=500) 
    else:
        raise Http404 