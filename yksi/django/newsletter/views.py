# load settings file
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
import os

#from .tasks import send_email

# import forms
from .forms import ContactForm, SignUpForm

#import send_mail

import json

# Create your views here.
def home(request):

#    if request.user.is_authenticated():
#        title = "My Title %s" %(request.user)
    #Test celery
    #add.delay(4, 5)

    if 'CF_INSTANCE_INDEX' in os.environ:
        CF_INSTANCE_INDEX = os.environ['CF_INSTANCE_INDEX']
    else:
        CF_INSTANCE_INDEX = 999

    if "VCAP_APPLICATION" in os.environ:
        application_name = json.loads(os.environ['VCAP_APPLICATION'])['application_name']
    else:
        application_name = "local"

    form = SignUpForm(request.POST or None)
    title = "Welcome on instance %s using app %s" %(CF_INSTANCE_INDEX, application_name)
    context = {
        "home": 'active',
        "title": title,
        "form": form,
        "index": CF_INSTANCE_INDEX,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.full_name:
            instance.full_name = "Empty"
        instance.save()
        context = {
            "home": 'active',
            "title": "Thank You!",
        }

    return render(request, "home.html", context)

def contact(request):
    title = "Contact:"
    form = ContactForm(request.POST or None)
    context = {
        "contact": 'active',
        "title": title,
        "form": form,
    }
    if form.is_valid():
        # for key, value in form.cleaned_data.items():
        #     print (key, value)
        # OR
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        #print (form_email, form_message, form_full_name)
        subject = 'Site contact form'
        from_email = form_email
        to_email = [settings.EMAIL_HOST_USER]
        contact_message = "%s: %s via %s" %(form_full_name, form_message, form_email)
        some_html_message = """
        <h1>This message was send to you from %s:</h1>
        %s
        """ %(form_full_name, form_message)
        # send asynchronous
        #send_email.delay(subject, contact_message, from_email, to_email, some_html_message)
        send_mail(subject,
                    contact_message,
                    from_email,
                    to_email,
                    html_message = some_html_message,
                    fail_silently = False)
        context = {
            "contact": 'active',
            "title": "Thank You!",
        }

    return render(request, "contact.html", context)
