from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


# celery send email
@shared_task
def send_verification_email_task(email, code):
    send_mail(
        subject="HI",
        message=f"Hello My Friend Your Verify Code {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
    return "Email sent"
