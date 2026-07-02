from django.urls import path
from .monitor import monitor_site, health_check
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("photo-upload/", views.photo_upload, name="photo_upload"),
    path("photo-delete/<int:id>/", views.photo_delete, name="photo_delete"),
    path("photo-edit/<int:id>/", views.photo_edit, name="photo_edit"),
    path("monitor-site/", monitor_site),
    path("user-gallery/<str:username>/", views.user_gallery, name="user_gallery"),
    path("health/", health_check, name='health-check'),
]
