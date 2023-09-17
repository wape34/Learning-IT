from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import News
from django.conf import settings


def send_notifications(description, pk, name, subscribers):
    html_content = render_to_string(
        'news_created_email.html',
    {'text': description,
     'link': f'{settings.SITE_URL}/news/{pk}',}
    )

    msg = EmailMultiAlternatives(
        subject=name,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(post_save, sender=News)
def notify_about_new_post(sender, instance, **kwargs):
    subscribers_emails = []
    subscribers = instance.category.subscribers.all()
    subscribers_emails += [s.email for s in subscribers]

    send_notifications(instance.description, instance.pk, instance.name, subscribers_emails)