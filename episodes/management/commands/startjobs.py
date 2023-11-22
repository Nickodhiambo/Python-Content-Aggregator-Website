# Standard Library imports
import logging

# Django imports
from django.conf import settings
from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from episodes.models import Episode

logger = logging.getLogger(__name__)

def save_new_episodes(feed):
    """
    Checks new feed IDs(GUID) against the IDs available in the database
    and adds only feeds with unique IDs.
    
    args:
        feed: An RSS feed object
    """
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                    title = item.title,
                    description = item.description,
                    pub_date = parser.parse(item.published),
                    link = item.link,
                    image = podcast_image,
                    podcast_name = podcast_title,
                    guid = item.guid,
                    )
            episode.save()

def fetch_real_python_episodes():
    """Retrieves episodes' data from realpython"""
    rp = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    save_new_episodes(rp)

def fetch_talk_python_episodes():
    """Retrieves episodes' from TalkPython"""
    tp = feedparser.parse("https://talkpython.fm/episodes/rss")
    save_new_episodes(tp)

def delete_old_job_executions(max_age=604_800):
    """Deletes podcast episodes older than a week"""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    """Custom Command to populate database with podcasts"""
    
    help = 'Runs scheduler'

    def handle(self, *args, **kwargs):
        """Runs the code that adds episodes to database"""
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
                fetch_real_python_episodes,
                trigger="interval",
                minutes=2,
                id="The Real Python Podcast",
                max_instances=1,
                replace_existing=True
                )
        logger.info("Added job: The Real Python Podcast.")

        scheduler.add_job(
                fetch_talk_python_episodes,
                trigger="interval",
                minutes=2,
                id="The Talk Python Podcast",
                max_instances=1,
                replace_existing=True
                )
        logger.info("Added job: The Talk Python Podcast.")

        scheduler.add_job(
                delete_old_job_executions,
                trigger=CronTrigger(
                    day_of_week='mon', hour='00', minute='00'
                    ), # Deleting old episodes starts on Monday midnight
                id='Delete Old Job Executions',
                max_instances=1,
                replace_existing=True,
                )
        logger.info('Added weekly job: Delete Old Job Executions.')

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler')
            scheduler.shutdown()
            logger.info('Scheduler shutdown successfully!')
