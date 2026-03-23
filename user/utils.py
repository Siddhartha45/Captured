import requests
from decouple import config


def send_verification_email(email, link, first_name):
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": config('BREVO_API_KEY'),
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {
            "name": "Captured",
            "email": config('BREVO_SENDER_EMAIL')
        },
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
            <p>If you did not create an account, ignore this email.</p>
        """
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 201