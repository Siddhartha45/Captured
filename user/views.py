from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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
            return render(request, 'user/signup.html', {'error':'password is too short.'})
        
        if not password1 == password2:
            return render(request, 'user/signup.html', {'error':'passwords do not match.'})
        
        user = User.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name, is_active = False)
        
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(f'/verify/{uid}/{token}/')
        send_mail(
            'Verify your email',
            f'Click this link to verify your email: {link}',
            None,
            [email],
            fail_silently=False,
        )

        return redirect('signin')
    return render(request, 'user/signup.html')

def verify_email(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(id=uid)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('signin')
    else:
        return HttpResponse("Invalid or expired verification link.")


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

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

def super_user_create(request):
    User.objects.create_superuser(email="admin@gmail.com", password="mount@8848")
    return HttpResponse("Super User Created")
