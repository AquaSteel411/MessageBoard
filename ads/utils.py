from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_notifications(preview, pk, title, subscribers, email, username, template):
    html_content = render_to_string(
        template,
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/ad/{pk}',
            'username': username,
            'email': email
        }

    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscribers]
    )

    message.attach_alternative(html_content, 'text/html')
    message.send()
