from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .utils import send_verification_email, password_reset_mail


User = get_user_model()


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            return render(request, 'user/signup.html', {'error':'Email already exists.'})

        if len(password1) < 8:
            return render(request, 'user/signup.html', {'error':'password is less than 8 characters.'})
        
        if not password1 == password2:
            return render(request, 'user/signup.html', {'error':'passwords do not match.'})
        
        user = User.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name, is_active = False)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f'/verify/{uid}/{token}/')
        # send_mail(
        #     'Verify your email',
        #     f'Click this link to verify your email: {link}',
        #     None,
        #     [email],
        #     fail_silently=False,
        # )
        send_verification_email(email, link, first_name)
        return redirect('signin')
    return render(request, 'user/signup.html')


def verify_email(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse("Account has been deleted")
    
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        return redirect('signin')
    else:
        return HttpResponse("Invalid or expired verification link.")


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'user/login.html', {'error': f'No account found with: {email}'})
            
        if not user.is_active:
            return render(request, 'user/login.html', {'error': 'Mail has been sent to you with verification link, Please verify and try again!'})
        
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user/login.html')


def signout(request):
    logout(request)
    return redirect('signin')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'user/forgot_password.html', {'error': 'Email does not exist!'})
        
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
        password_reset_mail(email, link, user.first_name)
        return redirect('signin')
    return render(request, 'user/forgot_password.html')


def password_reset(request, id, token):
    uid = urlsafe_base64_decode(id).decode()
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse("Invalid User")
    
    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid or expired link")

    if request.method == 'POST':
        p1 = request.POST.get("password1")
        p2 = request.POST.get("password2")
        
        if len(p1) < 8:
            return render(request, 'user/reset_password.html', {'error':'password is less than 8 characters.'})
        
        if p1 == p2:
            user.set_password(p1)
            user.save(update_fields=["password"])
            return redirect('signin')
        else:
            return render(request, 'user/reset_password.html', {'error': 'Passwords do not match'})
    return render(request, 'user/reset_password.html')


def resend_verification_mail(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Invalid User")
        
        if user.is_active:
            return render(request, 'user/resend_verification_mail.html', {'error': 'Your account is already verified.'})
        
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f'/verify/{uid}/{token}/')
        send_verification_email(email, link, user.first_name)
        return redirect('signin')
    return render(request, 'user/resend_verification_mail.html')