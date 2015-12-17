# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response

#from django.views.generic.edit import DeleteView
#from django.core.urlresolvers import reverse_lazy

from django.forms import modelformset_factory

from candidate.forms import CandidateFormSetHelper
from candidate.models import Candidate
from crispy_forms.layout import Submit

from myprofile.decorators import specific_verified_email_required

@specific_verified_email_required(domains=['emc.com','banck.net'])
def create(request):

    # validate user is authenticated
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect(reverse('login'))

    CandidateFormSet = modelformset_factory(Candidate, can_delete=True, fields=('first_name','last_name','photo','secure_photo'))
    helper = CandidateFormSetHelper()
    #helper.add_input(Submit("submit", "Save"))

    title = "Upload candidate picture"
    if request.method == 'POST':
        formset = CandidateFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('candidate-create'))
    else:
        formset = CandidateFormSet()

    context = {
        "candidate": 'active',
        "title": title,
        "formset": formset,
        "helper": helper,
    }
    #return render_to_response("candidate.html", context)
    return render(request, 'candidate.html', context)

    # if request.method == 'POST':
    #     form = CandidateForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('create'))
    # else:
    #     form = CandidateForm()
    # title = "Upload candidate picture"
    # # Load documents for the list page
    # candidates = Candidate.objects.all()
    #
    # context = {
    #     "title": title,
    #     "form": form,
    #     "candidates": candidates,
    # }
    # return render(request, 'candidate.html', context)
