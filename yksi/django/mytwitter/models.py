from django.db import models
from django.dispatch import receiver
from django.utils import timezone

import uuid

from yksi.custom_storages import SecureStorage

from easy_thumbnails.alias import aliases
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.signals import saved_file

#from .tasks import generate_thumbnails

# Create your models here.
class Tweet(models.Model):
    """( description)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    twitter_id = models.BigIntegerField(unique=True, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(max_length=160)
    created_at = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=15, blank=True)
    screenname = models.CharField(max_length=20, blank=True)
    from_twitter = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

def TweetPictureName(instance, filename):
    extension = filename.split('.')[-1]
    return '{}/{}.{}'.format('TweetPictures', str(uuid.uuid4()), extension)

class TweetPic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tweet = models.ForeignKey(Tweet, related_name='pics')
    picture = ThumbnailerImageField(upload_to=TweetPictureName, storage=SecureStorage(), thumbnail_storage=SecureStorage())
    def __str__(self):
        return str(self.picture.name)

from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)
#saved_file.connect(generate_thumbnails_async)

#@receiver(saved_file)
#def generate_thumbnails_async(sender, fieldfile, **kwargs):
#     generate_thumbnails.delay(model=sender, pk=fieldfile.instance.pk, field=fieldfile.field.name)
