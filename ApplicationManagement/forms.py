from django.forms import ModelForm, Form
from django.forms import inlineformset_factory, modelformset_factory, formset_factory

# Crispy Imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit, Reset, Layout, Field, MultiField, Div, Fieldset
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

# Import Models
from django.contrib.auth.models import User
from django import forms
from UserManagement.models import Team, TeamProfile
# Students
from UserManagement.models import Student, StudentProfile, Internship, Course, Competition, Award, Language
# Experts
from UserManagement.models import Student, ExpertProfile, MediationExperience, NegotiationExperience
# Staff
from UserManagement.models import Staff, StaffProfile

# ---- GENERAL PAGE RELEVANT FORMS ---------
class ApplicationSelection(Form):
    pass

class ContactForm(Form):
    sender = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# Define Forms
class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = []


# ----- TEAM REGISTRATION -------
class TeamRegistrationForm(ModelForm):
    class Meta:
        model = Team
        exclude = ['slug']


# ----- STUDENT REGISTRATION -------
class StdProfileForm_head(ModelForm):
    class Meta: 
        model = StudentProfile
        fields=['slogan', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('slogan', rows=3),
            Field('bio', rows=10),
        )


class StdProfileForm_side(ModelForm):
    class Meta:
        model = StudentProfile
        fields = (
            'profileImg',
            'country',
            'phoneNumber',
            'twitter',
            'linkedin',
            'facebook',
            'blog',

        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

class StdProfileForm_main(ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user', 'team', 'awards', 'internships', 'mediation_courses', 'negotiation_courses'] 

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper ()
        self.helper.form_class = "form-horizontal"
        self.helper.field_class = 'form-input-sm'
        self.helper.layout = Layout(
            Field('country', css_class='input-sm'),
            Field('phone', css_class='input-sm'),
            Field('country', css_class='input-sm'),
            Field('country', css_class='input-sm'),
            Field('country', css_class='input-sm'),
        )


    


# STUDENT ---- FormSets and Inline Formsets
class UserRegistrationForm(ModelForm):
    password_set = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ),
    label="Choose Password")
    password_repeat = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ),
    label="Confirm Password")
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','password_set', 'password_repeat']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ExpertProfileTop'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'


# STUDENT ----- LANGUAGES
class LanguageForm(ModelForm):
    class Meta:
        model = Language
        exclude = []

LanguageFormset = formset_factory(LanguageForm, extra=1)
class LanguageFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LanguageFormset_helper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(
                'name',
                Div(
                    'prof_written', 
                    css_class='col-sm-6'
                ),
                Div(
                    'prof_spoken',
                    css_class='col-sm-6',
                ),
                css_class='row experienceItem'
            )
        )
        self.render_required_fields = False

# STUDENT ---- INTERNSHIPS
class InternshipForm(ModelForm):
    class Meta:
        model = Internship
        exclude = []

InternshipFormset = formset_factory(InternshipForm, extra=1)
class InternshipFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InternshipFormset_helper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Div(
                Div(
                    'position',
                    css_class='col-sm-9',
                ),
                Div(
                    'field_of_practice',
                    'year',
                    'country',
                    'duration',
                    'languages_used',
                    css_class='col-sm-4',
                ),
                Div(
                    'employer',
                    Field('descr', rows=11),
                    css_class='col-sm-8',
                ),
                css_class=''
            )
        )


# STUDENT ------ COMPETITION EXPERIENCE
class CompetitionForm(ModelForm):
    class Meta:
        model = Competition
        exclude = []

CompetitionFormset = formset_factory(CompetitionForm, extra=1)
class CompetitionFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CompetitionFormset_helper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Div(
                'city',
                'country',
                'year',
                css_class='col-sm-4'
            ),
            Div(
                'name',
                'language',
                css_class='col-sm-8'
            )
        )

# STUDENT ------ COURSEWORK
class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = []
CourseworkFormset =  formset_factory(CourseForm, extra=1)
class CourseworkFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CourseworkFormset_helper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Div(
                'institution',
                'instructor',
                'duration',
                'measure',
                css_class='col-sm-4',
            ),
            Div(
                'title',
                'year',
                Field('learnings', rows='4'),
                css_class='col-sm-8',
            )
        )

# STUDENT ----- AWARDS & NOMINATIONS
class AwardForm(ModelForm):
    class Meta:
        model = Award
        exclude = []

AwardsFormset = inlineformset_factory(Competition, Award, exclude = [], extra=1)
class AwardsFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AwardsFormset_helper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Div('title',css_class='col-sm-8')
        )

TeamMemberRegistration = formset_factory(UserRegistrationForm, extra=1)


# --------------- EXPERT REGISTRATION ---------------------
class ExpertProfileForm(ModelForm):
    class Meta:
        model = ExpertProfile
        exclude = []

class ExpertProfileFormHeader(ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['slogan', 'bio']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ExpertProfileHeader'
        self.helper.layout = Layout(
            Field('slogan', rows=2)
        )

class ExpertProfileFormSide(ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['profileImg', 'affiliation', 'position', 'country', 'phoneNumber', 'twitter', 'linkedin', 'facebook', 'blog']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ExpertProfileSide'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            Field('profileImg', hidden=True)
        )

class ExpertProfileFormMain(ModelForm):
    class Meta:
        model = ExpertProfile
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ExpertProfileMain'

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

NegotiationExperienceFormset = formset_factory(NegotiationExperienceForm, extra=2)
class NegotiationExperienceFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NegotiationExperienceFormset_helper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
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

MediationExperienceFormset = formset_factory(MediationExperienceForm, extra=2) 
class MediationExperienceFormset_helper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MediationExperienceFormset_helper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
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
        self.add_input(Submit('submit', 'Save profile Information', css_class='profileSubmit btn-danger'))




# --- ASSESSMENT Forms ------------------------
"""
This section defines the relevant Forms used during the Assessment Process
"""
from ApplicationManagement.models import Review

class MemberReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = []
    
    def __init__(self, *args, **kwargs):
        super(MemberReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    

