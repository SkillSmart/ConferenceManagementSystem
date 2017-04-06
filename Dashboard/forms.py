from django import forms
from UserManagement.models import Attendent

# Model Imports
from ApplicationManagement.models import Application

# Crispy Addons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Button, ButtonHolder, Submit

# EXPERT MANAGEMENT ---------------
class ExpertCommentForm(forms.Form):
    comment = forms.CharField(
        label="Comments on Application", 
        max_length=250, 
        widget=forms.Textarea,
        required=False,
        )
    blacklisted = forms.BooleanField(required=False)
    status = forms.ChoiceField(
        label="Application Status",
        choices = Application.SELECTION_STATUS
    )

    def __init__(self, *args, **kwargs):
        super(ExpertCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save', css_class="btn-success"), )


class TeamCommentForm(forms.Form):
    comment = forms.CharField(
        label="Comments on Application", 
        max_length=250, 
        widget=forms.Textarea,
        required=False,
        )
    
    status = forms.ChoiceField(
        label="Application Status",
        choices = Application.SELECTION_STATUS
    )

    def __init__(self, *args, **kwargs):
        super(TeamCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save', css_class="btn-success"), )
        





