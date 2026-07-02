from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Photo
from .helpers import convert_heif_to_jpeg
import cloudinary.uploader

User = get_user_model()


def home(request):
    """photos posted by different users can be viewed here"""
    photos = Photo.objects.all()
    return render(request, "captured/home.html", {"image": photos})


def user_gallery(request, username):
    """users related photos"""
    user = User.objects.get(username=username)
    photos = Photo.objects.filter(user=user)

    context = {"image": photos, "profile_user": user}

    return render(request, "captured/user_gallery.html", context)


@login_required
def photo_upload(request):
    """page for uploading photo"""
    if request.method == "POST":
        image = request.FILES["image"]
        title = request.POST["title"]
        description = request.POST.get("description", "")

        content_type = image.content_type.lower()
        filename_ext = image.name.rsplit(".", 1)[-1].lower()
        HEIC_CONTENT_TYPES = {
            "image/heic",
            "image/heif",
            "image/x-heic",
            "image/x-heif",
        }
        HEIC_EXTENSIONS = {"heic", "heif"}

        if content_type in HEIC_CONTENT_TYPES or filename_ext in HEIC_EXTENSIONS:
            image = convert_heif_to_jpeg(image)

        # Upload to Cloudinary with dynamic folder
        upload_result = cloudinary.uploader.upload(
            image, folder=f"images/user_{request.user.id}"
        )

        Photo.objects.create(
            user=request.user,
            image=upload_result["public_id"],
            title=title,
            description=description,
        )

        messages.success(request, "Photo Uploaded.")
        return render(request, "captured/upload.html")

    return render(request, "captured/upload.html")


@login_required
def photo_delete(request, id):
    photo = get_object_or_404(Photo, id=id, user=request.user)
    photo.delete()
    return redirect("user_gallery", username=request.user.username)


@login_required
def photo_edit(request, id):
    photo = get_object_or_404(Photo, id=id, user=request.user)
    context = {"photo": photo}

    if request.method == "POST":
        photo.title = request.POST["title"]
        photo.description = request.POST.get("description", "")
        photo.save()
        return redirect("user_gallery", username=request.user.username)

    return render(request, "captured/edit_photo.html", context)
