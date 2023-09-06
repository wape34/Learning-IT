from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from project.news.models import NewsCategory
from project.project import settings


def send_notifications(prewiew, pk, title, subscribers):
    html_content = render_to_string(
        'news_created_email.html',
    {'text': prewiew,
     'link': f'{settings.SITE_URL}/news/{pk}',}
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=NewsCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'news_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.prewiew(), instance.pk, instance.title, subscribers_emails)