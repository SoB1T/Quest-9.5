import logging

from django.db.models import Count
from django.utils import timezone

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Post, Category

logger = logging.getLogger(__name__)


def send_notifications(subcribers, category_name, posts):
    # send_mail(f'{settings.DEFAULT_FROM_EMAIL}', "HI", f"{settings.DEFAULT_FROM_EMAIL}", ['retoreivszombe5@gmail.com'])
    html_contect = render_to_string(
        'mailsched.html',
        {
            'category_name': category_name,
            "posts": posts
        }

    )
    msg = EmailMultiAlternatives(
        subject="New post!",
        body=f"Dude, I've been trying to create an HTML letter template.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subcribers
    )
    msg.attach_alternative(html_contect, "text/html")

    msg.send()
    print("mail send")


# наша задача по выводу текста на экран
def my_job():
    start_date = timezone.now() - timezone.timedelta(days=7)
    categories_with_subscribers = Category.objects.annotate(num_subscribers=Count('subcribes')).filter(
        num_subscribers__gt=0)
    for category in categories_with_subscribers:
        recent_posts = Post.objects.filter(date__gte=start_date, categories=category)
        subscribers = category.subcribes.all()
        subscribers_emails = []
        for subs in subscribers:
            subscribers_emails.append(subs.email)
        if subscribers_emails and recent_posts:
            send_notifications(subscribers_emails, str(category), recent_posts)
        else:
            print("No new posts")


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),#(day_of_week="sun", hour="0", minute="0")
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
