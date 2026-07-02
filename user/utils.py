import requests
import uuid
from decouple import config
from django.contrib.auth import get_user_model


User = get_user_model()

# Configs for Brevo
url = "https://api.brevo.com/v3/smtp/email"
headers = {
    "accept": "application/json",
    "api-key": config("BREVO_API_KEY"),
    "content-type": "application/json",
}
sender = {"name": "Captured", "email": config("BREVO_SENDER_EMAIL")}


def send_verification_email(email, link, first_name):
    payload = {
        "sender": sender,
        "to": [
            {
                "email": email,
            }
        ],
        "subject": "Verify your account",
        "htmlContent": f"""
            <h2>Hello, {first_name}!</h2>
            <p>Thanks for signing up. Please verify your account by clicking the link below:</p>
            <a href="{link}" 
                style="background:#4CAF50;color:white;padding:10px 20px;
                    text-decoration:none;border-radius:5px;">
                Verify Email
            </a>
            <p>If you did not create an account, ignore this email. Please do not share this link with anyone!!!</p>
        """,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 201


def password_reset_mail(email, link, first_name):
    payload = {
        "sender": sender,
        "to": [
            {
                "email": email,
            }
        ],
        "subject": "Reset your password",
        "htmlContent": f"""
            <h2>Hello, {first_name}!</h2>
            <p>You have requested for password reset. Click the link below to reset your password:</p>
            <a href="{link}" 
                style="background:#4CAF50;color:white;padding:10px 20px;
                    text-decoration:none;border-radius:5px;">
                Verify Email
            </a>
            <p>Please do not share this link with anyone!!!</p>
        """,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 201


def generate_username(first_name):
    """randomly generates username with 10 characters."""
    while True:
        username = first_name.lower().strip().replace(" ", "") + uuid.uuid4().hex[:5]
        if not User.objects.filter(username=username).exists():
            return username

