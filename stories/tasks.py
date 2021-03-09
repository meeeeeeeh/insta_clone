from celery import shared_task
from .models import StoryStream, Story
from datetime import timedelta, datetime


@shared_task
def check_stories_date():
    exp_date = datetime.now() - timedelta(hours=1)
    old_stories = Story.objects.filter(posted__lt=exp_date)
    old_stories.update(expired=True)
    print("stories updated")


@shared_task
def delete_old_stories():
    Story.objects.filter(expired=True).delete()
    StoryStream.objects.filter(story=None).delete()