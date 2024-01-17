from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from django.conf import settings


def send_notifications(heading, id, text, subcribers):
    html_contect = render_to_string(
        'mailcat.html',
        {'text': heading,
         'link': f'{settings.SITE_URL}/posts/{id}'

         }

    )
    msg = EmailMultiAlternatives(
        subject=text,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subcribers
    )
    msg.attach_alternative(html_contect, "text/html")


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs["action"] == "post.add":
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]
        send_notifications(instance.heading(), instance.id, instance.text, subscribers_emails)
