from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('photo-upload/', views.photo_upload, name='photo_upload'),
    path('user-photos/', views.user_upload_list, name='user_photos'),
    path('photo-delete/<int:id>/', views.photo_delete, name='photo_delete'),
    path('photo-edit/<int:id>/', views.photo_edit, name='photo_edit'),
]