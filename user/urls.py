from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("verify/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<id>/<token>/", views.password_reset, name="password_reset"),
    path(
        "resend-verification-mail/",
        views.resend_verification_mail,
        name="resend_verification_mail",
    ),
]
