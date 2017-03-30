from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.forms.models import formset_factory, modelform_factory, inlineformset_factory

# Crispy Imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

# Profile Models
from Authentication.forms import UserModelForm
from .models import ExpertProfile, TeamProfile, StudentProfile, Program
# Expert Attribute Models
from .models import MediationExperience, NegotiationExperience
# Student Attribute Models
from .models import Internship, Course, Award

# # Setting up the forms
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ExpertModelForm(ModelForm):
    class Meta:
        model = ExpertProfile
        exclude = ['user']        

class TeamModelForm(ModelForm):
    class Meta:
        model = TeamProfile
        exclude = ['member_a', 'member_b', 'coach_a', 'coach_b']
        fields = []
        
class StudentModelForm(ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['attendent', 'mediation_courses', 'negotiation_courses']

# Attribute Forms Student Attendents
class InternshipForm(ModelForm):
    class Meta:
        model = Internship
        exclude = []

class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude=[]

class AwardForm(ModelForm):
    class Meta:
        model = Award
        exclude = []

#------------ EXPERT PROFILE FORMS ------------------------

class MediationExperienceForm(ModelForm):
    class Meta:
        model = MediationExperience
        fields = ['profession', 'duration', 'cases', 'description', 'priorClients', 'placesWorked']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class NegotiationExperienceForm(ModelForm):
    class Meta:
        model = NegotiationExperience
        fields = ['profession', 'duration', 'cases', 'description', 'priorClients', 'placesWorked']

    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()

#EXPERT _ FORMSETS AND INLINE FORMSETS
ProgramFormSet = inlineformset_factory(ExpertProfile, Program, exclude=[], extra=2)
class ProgramFormSet_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    'subject',
                    'startDate',
                    'endDate',
                    'institution',
                    Field('priorClients', rows=3),
                    Field('placesWorked', rows=3),
                    css_class='col-sm-4'
                ),
                Div(
                    'title',
                    'description',
                    css_class='col-sm-8',
                ),
                css_class='row experienceItem'
                )
            )
        self.render_required_fields = False

NegotiationExperienceFormset = inlineformset_factory(ExpertProfile, NegotiationExperience, extra=2, exclude=[])
class NegotiationExperienceFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    'duration',
                    'cases',
                    Field('priorClients', rows=3),
                    Field('placesWorked', rows=3),
                    css_class='col-sm-4'
                ),
                Div(
                    'profession',
                    'description',
                    css_class='col-sm-8',
                ),
                css_class='row experienceItem'
                )
            )
        self.render_required_fields = False

MediationExperienceFormset = inlineformset_factory(ExpertProfile, MediationExperience, extra=2, exclude=[]) 
class MediationExperienceFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MediationExperienceFormset_helper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                'duration',
                'cases',
                Field('priorClients', rows=3),
                Field('placesWorked', rows=3),
                css_class='col-sm-4'
            ),
            Div(
                'profession', 
                'description', 
                css_class='col-sm-8',
            ),
            css_class='row experienceItem'
            )
        )
