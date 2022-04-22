from django.core.mail import send_mail
#
#
# def send_activation_code(email, activation_code):
#     activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
#     message = f"""
#         Вы успешно зарегестрировались,
#         пожалуйста подтвердите что это ваша почта.
#         нажмите сюда {activation_url}
#     """
#     send_mail(
#         'активируйте свой аккаунт',
#         message,
#         'test@gmail.com',
#         [email, ],
#         fail_silently=False
#     )


def send_confirmation_email(activation_code, email):
    full_link = f'http://localhost:8000/v1/api/account/activate/{activation_code}'

    send_mail(
        'Привет',
        full_link,
        'osmonalievadilet10@gmail.com',
        [email]
    )