from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# for testing only mail
from django.http import HttpResponse
import socket

from .models import Photo
from .helpers import convert_heif_to_jpeg
import cloudinary.uploader

User = get_user_model()

@login_required
def home(request):
    image = Photo.objects.filter(user=request.user)

    context = {'image':image}

    return render(request, 'captured/index.html', context)

@login_required
def photo_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        title = request.POST['title']
        description = request.POST.get('description', '')

        # jpeg_image = convert_heif_to_jpeg(image)
        if image.content_type in ['image/heic', 'image/heif']:
            image = convert_heif_to_jpeg(image)
        
        # Upload to Cloudinary with dynamic folder
        upload_result = cloudinary.uploader.upload(
            image,
            folder=f'images/user_{request.user.id}'
        )

        Photo.objects.create(user=request.user, image=upload_result['public_id'], title=title, description=description)
        
        return render(request, 'captured/photo_upload.html', {'success':'Photo Uploaded.'})

    return render(request, 'captured/photo_upload.html')

@login_required
def user_upload_list(request):
    photos = Photo.objects.filter(user=request.user)

    context = {'photos':photos}
    return render(request, 'captured/user_photos.html', context)

@login_required
def photo_delete(request, id):
    photo = Photo.objects.get(id=id)
    photo.delete()
    return redirect('user_photos')

@login_required
def photo_edit(request, id):
    photo = Photo.objects.get(id=id, user=request.user)
    context = {'photo': photo}

    if request.method == 'POST':
        photo.title = request.POST['title']
        photo.description = request.POST.get('description', '')
        photo.save()
        return redirect('user_photos')
    
    return render(request, 'captured/photo_edit.html', context)

def grand_home(request):
    """even non authenticated users can see others photos"""
    photos = Photo.objects.all()
    return render(request, 'captured/grand_home.html', {'image':photos})




def test_email(request):
    try:
        socket.setdefaulttimeout(5)
        sock = socket.create_connection(('smtp.gmail.com', 587), timeout=5)
        sock.close()
        port_587 = "Port 587 reachable"
    except Exception as e:
        port_587 = f"Port 587 BLOCKED: {e}"

    try:
        sock = socket.create_connection(('smtp.gmail.com', 465), timeout=5)
        sock.close()
        port_465 = "Port 465 reachable"
    except Exception as e:
        port_465 = f"Port 465 BLOCKED: {e}"

    try:
        from django.core.mail import send_mail
        send_mail('Test', 'Test body', None, ['sanjivr361@gmail.com'], fail_silently=False)
        mail_result = "Mail sent successfully"
    except Exception as e:
        mail_result = f"Mail failed: {e}"

    return HttpResponse(f"""
        {port_587}<br>
        {port_465}<br>
        {mail_result}
    """)