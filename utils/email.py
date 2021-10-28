import io

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def example(subject='Hello', recipient_list=['belyaev@raketa.im']):
    """
    Пример отправки письма html с пложениями файлов с сервера и из памяти
    """
    html_message = render_to_string('mail_template.html', {'context': 'values'})
    mail = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_FROM, to=recipient_list)
    mail.attach_alternative(html_message, 'text/html')
    mail.attach('file_from_memory.txt', io.StringIO("some initial binary data: \x00\x01").read())
    mail.send()
