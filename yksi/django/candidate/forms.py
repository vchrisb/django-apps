from django import forms
from candidate.models import Candidate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

class CandidateFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CandidateFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.form_action = 'candidate-create'
        self.add_input(Submit('submit', 'Submit'))
