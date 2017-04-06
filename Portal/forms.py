from django import forms
from UserManagement.models import Student, Expert, Staff, Team

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field

# -- EXPERT Section ------
class ExpertSearchForm(forms.Form):
    name = forms.CharField(max_length=150)
    nationality = forms.CharField(max_length=100)
    languages = forms.CharField(max_length=100)
    affiliation = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(ExpertSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal form-sm'
        self.helper.add_input(Submit('search expert', 'Search expert', css_class='btn-success'))
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9'

# ---- TEAM Section ------
class TeamSearchForm(forms.Form):
    name = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    role = forms.CharField(max_length=100)

class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['role','administrativeComment','blacklisted', 'slug', 'user']