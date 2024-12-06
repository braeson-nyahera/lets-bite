from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

def send_registration_email(user : CustomUser):
    subject = "Successful Registration to lets_bite"
    message = f"""
    Dear {user.username.capitalize()},

    Thank you for registering to Lets_bite. We hope your expectations will be met by our five star services.

    Best regards,
    Lets_bite team
    """

    send_mail(
        subject,message,settings.EMAIL_HOST_USER, recipient_list = [user.email]
    )