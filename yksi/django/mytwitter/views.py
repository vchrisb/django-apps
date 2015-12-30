from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import TweetForm
from .models import Tweet, TweetPic
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myprofile.decorators import specific_verified_email_required

@transaction.atomic
@specific_verified_email_required(domains=['emc.com','banck.net', 'domain.local'])
def tweet(request):
    title = "Tweet:"
    tweet_list = Tweet.objects.all().order_by('-created_at')[:100]
    paginator = Paginator(tweet_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')

    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tweets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tweets = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            for picture in form.cleaned_data['picture']:
                TweetPic.objects.create(picture=picture, tweet=instance)

            return HttpResponseRedirect(reverse('tweet'))

    form = TweetForm()
    context = {
        "tweet": 'active',
        "title": title,
        "form": form,
        "tweets": tweets,
    }
    return render(request, "tweet.html", context)

@specific_verified_email_required(domains=['emc.com','banck.net', 'domain.local'])
def TweetPicView(request, uuid):
    TweetPicObj = get_object_or_404(TweetPic, pk=uuid)
    return HttpResponseRedirect(TweetPicObj.picture.url)
