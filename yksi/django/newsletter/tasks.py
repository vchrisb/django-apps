from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(subject, contact_message, from_email, to_email, html_message):
    send_mail(subject,
                contact_message,
                from_email,
                to_email,
                html_message = html_message,
                fail_silently = False)
