from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('super/', views.super_user_create, name='super'),
]