from django.urls import path
from .monitor import monitor_site
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("photo-upload/", views.photo_upload, name="photo_upload"),
    path("user-photos/", views.user_upload_list, name="user_photos"),
    path("photo-delete/<int:id>/", views.photo_delete, name="photo_delete"),
    path("photo-edit/<int:id>/", views.photo_edit, name="photo_edit"),
    path("", views.grand_home, name="grand_home"),
    path("monitor-site/", monitor_site),
    # path('test-email/', views.test_email),
]
