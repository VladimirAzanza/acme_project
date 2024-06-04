from datetime import date

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

def real_age(value: date) -> None:
    age = (date.today() - value).days / 365
    if age < 1 or age > 120:
        send_mail(
                subject='Bad Entry',
                message=(
                    f'Вы питались выбрать неверную дату.'
                    f'Возраст для выбранной записи: {int(age)}'
                ),
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )
