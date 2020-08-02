from .backend.models import ClientProfile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_welcome_email(user, password):
    client = ClientProfile.objects.get(user=user)
    message = render_to_string('emails/send_mails.html', {
                    'type': 'welcome',
                    'user': client.user,
                    'password': password,
                })
    mail_subject = 'Welcome to Payloop..last step remaining'
    to_email = client.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()


def send_notification(user_id):
    client = ClientProfile.objects.get(user_id=user_id)
    message = render_to_string('emails/send_mails.html', {
        'type': 'notify_staff',
        'user': client.user,
    })
    mail_subject = 'New registration from payloop'
    to_email = 'enquiries@payloop.net'
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()
