from django import forms
from .models import Tweet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'picture']

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Tweet'))
        self.helper.form_method = 'post'
        self.helper.form_action = 'tweet'
        self.helper.layout = Layout(
            Field('text', rows="6")
            )


class TweetAdminForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['user', 'username', 'screenname', 'text', 'picture']
