from django.shortcuts import render, redirect
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .utils import send_verification_email, password_reset_mail, generate_username

User = get_user_model()


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "auth/signup.html")

        if len(password1) < 8:
            messages.error(request, "password is less than 8 characters.")
            return render(
                request,
                "auth/signup.html",
            )

        if not password1 == password2:
            messages.error(request, "passwords do not match.")
            return render(request, "auth/signup.html")

        user = User.objects.create_user(
            email=email,
            username=generate_username(first_name),
            password=password1,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f"/verify/{uid}/{token}/")
        # send_mail(
        #     'Verify your email',
        #     f'Click this link to verify your email: {link}',
        #     None,
        #     [email],
        #     fail_silently=False,
        # )
        send_verification_email(email, link, first_name)
        messages.success(request, "Account created. ")
        return redirect("signin")
    return render(request, "auth/signup.html")


def verify_email(request, uidb64, token):
    """sets user to active so they can log in."""
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse("Account has been deleted")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        return redirect("signin")
    else:
        return HttpResponse("Invalid or expired verification link.")


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, f"No account found with: {email}")
            return render(request, "auth/signin.html")

        if not user.is_active:
            messages.info(
                request,
                "Mail has been sent to you with verification link, Please verify and try again!",
            )
            return render(request, "auth/signin.html")

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "auth/signin.html")
    return render(request, "auth/signin.html")


def signout(request):
    logout(request)
    return redirect("signin")


def forgot_password(request):
    """mail get sent to user's email to reset their password."""
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email does not exist!")
            return render(request, "auth/forgot_password.html")

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f"/reset-password/{uid}/{token}/")
        
        password_reset_mail(email, link, user.first_name)
        messages.success(request, "Password reset link has been sent to your email.")
        return redirect("signin")
    
    return render(request, "auth/forgot_password.html")


def password_reset(request, id, token):
    """page where user can reset their password if they forget it."""
    uid = urlsafe_base64_decode(id).decode()
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse("Invalid User")

    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid or expired link")

    if request.method == "POST":
        p1 = request.POST.get("password1")
        p2 = request.POST.get("password2")

        if len(p1) < 8:
            messages.error(request, "password is less than 8 characters.")
            return render(request, "auth/password_reset.html")

        if p1 == p2:
            user.set_password(p1)
            user.save(update_fields=["password"])
            messages.success(request, "Password reset complete.")
            return redirect("signin")
        else:
            messages.error(request, "Passwords do not match")
            return render(request, "auth/password_reset.html")
    return render(request, "auth/password_reset.html")


def resend_verification_mail(request):
    """mail gets sent to user's email if their verification link is inavlid."""
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Invalid User")

        if user.is_active:
            messages.info(request, "Your account is already verified. You can log in.")
            return render(
                request,
                "auth/resend_verification.html",
            )

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f"/verify/{uid}/{token}/")
        
        send_verification_email(email, link, user.first_name)
        messages.success(request, "Verification link has been sent to your email.")
        return redirect("signin")

    return render(request, "auth/resend_verification.html")


@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = User.objects.get(id=request.user.id)

        if len(new_password) < 8:
            messages.error(request, "password is less than 8 characters.")
            return render(request, "auth/change_password.html")

        if new_password != confirm_password:
            messages.error(request, "new passwords do not match.")
            return render(request, "auth/change_password.html")

        if new_password == current_password:
            messages.error(
                request, "current password and new password cannot be the same."
            )
            return render(request, "auth/change_password.html")

        if not user.check_password(current_password):
            messages.error(request, "Your current password is incorrect.")
            return render(request, "auth/change_password.html")

        user.set_password(new_password)
        user.save(update_fields=["password"])
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully.")
        return redirect("change_password")

    return render(request, "auth/change_password.html")
