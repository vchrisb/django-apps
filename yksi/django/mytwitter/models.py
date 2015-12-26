from django.db import models
from yksi.custom_storages import SecureStorage

from django.dispatch import receiver
from easy_thumbnails.signals import saved_file

from easy_thumbnails.alias import aliases
from easy_thumbnails.fields import ThumbnailerImageField

#from .tasks import generate_thumbnails

# Create your models here.
class Tweet(models.Model):
    """( description)"""
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    username = models.CharField(max_length=15, blank=True)
    screenname = models.CharField(max_length=20, blank=True)
    text = models.TextField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True, auto_now = False)
    picture = ThumbnailerImageField(blank=True, null=True, upload_to='tweet-pictures', storage=SecureStorage(), thumbnail_storage=SecureStorage())
    from_twitter = models.BooleanField(default=False)
    # def save(self, *args, **kwargs):
    #     if self.user:
    #         self.username = self.user
    #     super(Subject, self).save(*args, **kwargs)

# class TweetPicture(models.Model):
#     tweet = models.ForeignKey(Tweet)
#     picture = ThumbnailerImageField(upload_to='TweetPictures', storage=SecureStorage(), thumbnail_storage=SecureStorage())

from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)
#saved_file.connect(generate_thumbnails_async)

#@receiver(saved_file)
#def generate_thumbnails_async(sender, fieldfile, **kwargs):
#     generate_thumbnails.delay(model=sender, pk=fieldfile.instance.pk, field=fieldfile.field.name)
