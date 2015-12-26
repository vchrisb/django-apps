from django.shortcuts import render

# Create your views here.
from .forms import TweetForm
from .models import Tweet

from myprofile.decorators import specific_verified_email_required

@specific_verified_email_required(domains=['emc.com','banck.net'])
def tweet(request):
    title = "Tweet:"
    tweets = Tweet.objects.all().order_by('-created_at')[:100]

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            #if not instance.full_name:
            #    instance.full_name = "Empty"
            instance.user = request.user
            instance.save()

    form = TweetForm()
    context = {
        "contact": 'active',
        "title": title,
        "form": form,
        "tweets": tweets,
    }
    return render(request, "tweet.html", context)
