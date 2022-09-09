from django.core.mail import send_mail
from .models import Contact

def send_confirmation_email(user,code):
    code = code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email = user
    send_mail(
        'Здравствуйте активирует ваш аккаунт !!!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке {full_link}',
        'babaevermek72@gmail.com',
        [to_email,],
        fail_silently=False

        )
def send_reset_password(user,code):
    code = code
    to_email = user
    send_mail('Sibject',
    f'Your code for reset password:{code}',
    'from@example.com',
    [to_email,],
    fail_silently=False
)
def sending_message():
    full_link =  f'http://localhost:8000/api/v1/video/'
    for user in Contact.objects.all():
        send_mail(
            'My movies',
            f'Загляни на наш сайт,у нас есть новинки: {full_link} ',
            'igor123456yartsev@gmail.com',
            [user.email],
            fail_silently=False,
        )

