from .celery import app
from account.send_email import send_confirmation_email,send_reset_password,sending_message
from django.core.mail import send_mail
from account.models import Contact


@app.task
def send_email_task(to_email,code):
    send_confirmation_email(to_email,code)

@app.task
def send_reset_email_task(to_email,code):
    send_reset_password(to_email,code)

@app.task
def sending_message_task():
    sending_message()


