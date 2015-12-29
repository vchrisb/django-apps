from __future__ import absolute_import

from celery import shared_task

from .models import Tweet
import uuid
from django.core.files.base import ContentFile

@shared_task
def print_url(tweet):
    print(tweet['text'])

@shared_task
def save_tweet(tweetobj):
    username = tweetobj['user']['name']
    screenname = tweetobj['user']['screen_name']
    text = tweetobj['text']
    created_at = tweetobj['created_at']
    image = None
    try:
        if tweetobj['entities']['media'][0]['type'] == 'photo':
            image = retrieve_image(tweetobj['entities']['media'][0]['media_url'] + ":large")
            # cut image url  from tweet text
            text = text.replace(tweetobj['entities']['media'][0]['url'],"")
    except KeyError:
        pass
        #return  # no picture
    # create tweet
    newtweet = Tweet(username=username, screenname=screenname, text=text, created_at=created_at, from_twitter=True)

    if image is not None:
        image = process_image(image)
        image_name = str(uuid.uuid4()) + ".jpg"
        newtweet.picture.save(image_name,image)

    newtweet.save()

    print("saved tweet with id " + str(tweetobj['id']))

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
