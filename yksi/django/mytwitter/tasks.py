from __future__ import absolute_import

from celery import shared_task
from easy_thumbnails.files import generate_all_aliases
from .models import Tweet, TweetPic
import uuid
import pytz
from django.utils import timezone
from django.core.files.base import ContentFile
from django.db import transaction
from easy_thumbnails.files import generate_all_aliases
from tweepy.utils import parse_datetime

@shared_task
def print_url(tweet):
    print(tweet['text'])

@shared_task
@transaction.atomic
def save_tweet(tweetobj):
    twitter_id = tweetobj['id']
    username = tweetobj['user']['name']
    screenname = tweetobj['user']['screen_name']
    text = tweetobj['text']
    created_at = parse_datetime(tweetobj['created_at'])
    created_at = timezone.make_aware(created_at, timezone=pytz.UTC) #tweets are stored int UTC

    image_urls = []
    try:
        for media in tweetobj['entities']['media']:
            if media['type'] == 'photo':
                image_urls.append(media['media_url'] + ":large")
                # cut image url  from tweet text
                text = text.replace(media['url'],"")
    except KeyError:
        pass
        # print("no picture")
        # return  # no picture

    # if len(image_list) < 2:
    #     print ("less than 2 pictures" + str(len(image_list)))
    #     return
    # create tweet
    newtweet = Tweet(twitter_id=twitter_id, username=username, screenname=screenname, text=text, created_at=created_at, from_twitter=True)
    newtweet.save()
    if image_urls:
        for image_url in image_urls:
            #print(image_url)
            image = retrieve_image(image_url)
            image = process_image(image) # returns jpg
            image_name = "tmp.jpg" # will be renamed by model save function
            newpic = TweetPic()
            newpic.tweet = newtweet
            newpic.picture.save(image_name,image)
            newpic.save()
            generate_all_aliases(newpic.picture, include_global=True) # create thumbnails

    print("saved tweet with id %s" %(str(twitter_id)))

@shared_task
def generate_thumbnails(model, pk, field):
    print('generate thumb task')
    instance = model._default_manager.get(pk=pk)
    fieldfile = getattr(instance, field)
    generate_all_aliases(fieldfile, include_global=True)

import urllib.request
from PIL import ImageFilter, Image
def retrieve_image(image_url):
    """
    Retrieves the image from the web
    """
    im = None
    try:
        im = Image.open(urllib.request.urlopen(image_url))  #Try to get the image, but if it fails
    except IOError as e:
        return None
    return im

import io
def process_image(image):
    image_io = io.BytesIO()
    image.save(image_io, 'jpeg')  #store it as a JPG
    #image_io.seek(0)
    image = ContentFile(image_io.getvalue())
    #image = Image.open(buf)
    return image  #and give back the image
