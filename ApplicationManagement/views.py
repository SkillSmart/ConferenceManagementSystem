from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import transaction
from django.conf import settings

# MODEL Imports ---------
from ApplicationManagement.models import Application, Attendent
from UserManagement.models import ExpertProfile

# GENERIC VIEWS -----------
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# FORM Imput -----------
from django.forms import ChoiceField
from .forms import (ContactForm,
                    AttendentModelForm,
                    UserRegistrationForm)
# ----  STUDENT FORMS  -------------
from .forms import (StudentProfileForm,
                    StdProfileForm_head,
                    StdProfileForm_head_side,
                    StdProfileForm_main,
                    StdProfileForm_side)
# student___Formsets
from .forms import (LanguageFormset,
                    InternshipFormset,
                    CompetitionFormset,
                    CourseworkFormset,
                    AwardFormset)
# student___Formset Helper 
from .forms import (LanguageFormset_helper,
                    InternshipFormset_helper,
                    CompetitionFormset_helper,
                    CourseworkFormset_helper,
                    AwardFormset_helper)
# ---  EXPERT FORMS  -------------
from .forms import (ExpertProfileForm,
                    ExpertProfileFormHeader,
                    ExpertProfileFormHeaderSide,
                    ExpertProfileFormMain,
                    ExpertProfileMembershipForm,
                    ExpertProfileFormSide)
# expert___Formsets
from .forms import (MediationExperienceFormset,
                    NegotiationExperienceFormset)
#expert___FormHelper
from .forms import (MediationExperienceFormset_helper,
                    NegotiationExperienceFormset_helper)
# ----  TEAM FORMS  -------------
from .forms import (TeamRegistrationForm,
                    TeamMemberRegistration)
# ----  STAFF FORMS  -------------
# from .forms import ()

# ---  ASSESSMENT Forms -------
from .forms import MemberReviewForm

# General Informa



# ------Application Process Forms ---------
def user_registration(request):
    return render(request, 'application/registration.html', {
    })

class AccountRegistrationView(View):
    # Helper Methods for Form handling
    def check_valid(self, *args):
        for form in args:
            if not form.is_valid():
                return False
            return True

    def forward_next(self, role):
        """Determines the logic where to forward based on the role chosen"""
        if role == 'student':
            return HttpResponseRedirect('/application/student')
        if role == "expert":
            return HttpResponseRedirect('/application/expert/')
        if role == "staff":
            return HttpResponseRedirect('/application/staff/')
        if role == "team":
            return HttpResponseRedirect('/application/team/')
        else:
            return HttpResponseRedirect('/')

    def get_choices(self, role):
        if role == 'expert':
            return settings.EXPERT_ROLES
        elif role == 'student':
            return settings.STUDENT_ROLES
        elif role == 'staff':
            return settings.STAFF_ROLES
        else:
            return None


    # Handling the Http Requests
    def get(self, request, role):
        # Set the forms
        user_form = UserRegistrationForm()
        attendent_form = AttendentModelForm(choices=self.get_choices(role))

        return render(request, 'application/register_account.html', {
            'user_form': user_form,
            'attendent_form': attendent_form, 
            'role': role, 
        })

    def post(self, request, role):
        user_form = UserRegistrationForm(request.POST)
        attendent_form = AttendentModelForm(request.POST)

        if self.check_valid(user_form, attendent_form):
            # Create user object and add the username to it
            user = user_form.save(commit=False)
            user.set_password(request.POST['password'])
            user.username = "{}.{}".format(user.first_name, user.last_name)
            # Save the attendent form for the user created
            attendent = attendent_form.save(commit=False)
            attendent.role = request.POST['role']

            # If everything so far worked, save
            user.save()
            # user.set_password(user_form.cleaned_data['password_set'])
            attendent.user = user
            attendent.save()

            # Loging the person into the system and continuing to profile creation
            login(request, user)
            # Then finally redirect to the appropriate place
            return self.forward_next(role)
        else:
            return render(request, 'application/register_account.html', {
                'user_form': user_form, 
                'attendent_form': AttendentModelForm(choices=self.get_choices(role)),
            })


class ExpertRegistrationView(View):

    def check_valid(self, forms_list):
        for form in forms_list:
            if not form.is_valid():
                return False
        return True

    def get(self, request):
        profileFormHeader = ExpertProfileFormHeader()
        profileFormHeaderSide = ExpertProfileFormHeaderSide()
        profileFormSide = ExpertProfileFormSide()
        profileFormMain = ExpertProfileFormMain()
        profileFormMembership = ExpertProfileMembershipForm()
        # mediationExp = MediationExperienceFormset()
        # negotiationExp = NegotiationExperienceFormset()

        return render(request, 'application/expert_application.html', {
            'user': request.user,
            'profileFormHeader': profileFormHeader,
            'profileFormHeaderSide': profileFormHeaderSide,
            'profileFormSide': profileFormSide,
            'profileFormMain': profileFormMain,
            'profileFormMembership': profileFormMembership,
            # 'mediationExp': mediationExp,
            # 'mediationExp_helper': MediationExperienceFormset_helper(),
            # 'negotiationExp': negotiationExp,
            # 'negotiationExp_helper': NegotiationExperienceFormset_helper(),
        })

    def post(self, request):
        # Instantiate the Forms:
        profileFormHeader = ExpertProfileFormHeader(request.POST)
        profileFormHeaderSide = ExpertProfileFormHeaderSide(request.POST, request.FILES)
        profileFormSide = ExpertProfileFormSide(request.POST)
        profileFormMain = ExpertProfileFormMain(request.POST)
        profileFormMembership = ExpertProfileMembershipForm(request.POST)
        # mediationExp = MediationExperienceFormset(request.POST)
        # negotiationExp = NegotiationExperienceFormset(request.POST)

        # Instantiate the overall form
        profile = ExpertProfileForm(request.POST, request.FILES)
        if profile.is_valid():
            # Save the Expert Application Form
            this = profile.save(commit=False)
            this.attendent = Attendent.objects.get(user=request.user)
            this.save()

            # if yes, redirect to the profile view
            return HttpResponseRedirect('/profile')
        else:
            # Redisplay Form with Errors attached
            return render(request, 'application/expert_application.html', {
                'user': request.user,
                'profileFormHeader': profileFormHeader,
                'profileFormHeaderSide': profileFormHeaderSide,
                'profileFormSide': profileFormSide,
                'profileFormMain': profileFormMain,
                'profileFormMembership': profileFormMembership,
                # 'mediationExp': mediationExp,
                # 'mediationExp_helper': MediationExperienceFormset_helper(),
                # 'negotiationExp': negotiationExp, 
                # 'negotiationExp_helper': NegotiationExperienceFormset_helper(),
            })


class StudentRegistrationView(View):

    def check_valid(self, *args, **kwargs):
        for form in args:
            if not form.is_valid():
                return False
        return True

    def get(self, request):
        # Student Profile Forms
        profileFormHeader = StdProfileForm_head()
        profileFormHeaderSide = StdProfileForm_head_side()
        profileFormSide = StdProfileForm_side()
        profileFormMain = StdProfileForm_main()
        # Many to many Formsets
        languageFormset = LanguageFormset(prefix='lngFs')
        internshipFormset = InternshipFormset(prefix='intFs')
        competitionFormset = CompetitionFormset(prefix='cmpFs')
        courseworkFormset = CourseworkFormset(prefix='cswFs')
        awardFormset = AwardFormset(prefix='awdFs')

        return render(request, 'application/student_application.html', {
            'user': request.user,
            # Student Profile Forms
            'profileFormHeader': profileFormHeader,
            'profileFormHeaderSide': profileFormHeaderSide,
            'profileFormSide': profileFormSide,
            'profileFormMain': profileFormMain,
            # Many to Many Formsets
            'languageFormset': languageFormset,
            'competitionFormset': competitionFormset,
            'internshipFormset': internshipFormset,
            'courseworkFormset': courseworkFormset,
            'awardFormset': awardFormset,
            # Formset Helper
            'languageFormset_helper': LanguageFormset_helper(),
            'internshipFormset_helper': InternshipFormset_helper(),
            'competitionFormset_helper': CompetitionFormset_helper(),
            'courseworkFormset_helper': CourseworkFormset_helper(),
            'awardFormset_helper': AwardFormset_helper(),
        })

    def post(self, request):
        # Student Profile Forms
        profileFormHeader = StdProfileForm_head(request.POST)
        profileFormHeaderSide = StdProfileForm_head_side(request.POST, request.FILES)
        profileFormSide = StdProfileForm_side(request.POST)
        profileFormMain = StdProfileForm_main(request.POST)
        # Many To Many Formsets
        internshipFormset = InternshipFormset(request.POST, prefix='intFs')
        competitionFormset = CompetitionFormset(request.POST, prefix='cmpFs')
        courseworkFormset = CourseworkFormset(request.POST, prefix='cswFs')
        languageFormset = LanguageFormset(request.POST, prefix='lngFs')
        # awardFormset = AwardFormset(request.POST, prefix='awdFs')

        # Combine in StudentProfileForm
        profile = StudentProfileForm(request.POST, request.FILES)

        if self.check_valid(profile, competitionFormset, languageFormset):
            profile_inst = profile.save(commit=False)
            profile_inst.attendent = Attendent.objects.get(user=request.user)
            profile_inst.save()

            # Create all Competition Instances, and update them in bulk
            new_compExp = []
            for form in competitionFormset():
                compExp = form.save(commit=False)
                compExp.profile = profile_inst
                compExp.save()



            # try:
            #     with transaction.atomic():
            #         # Replace all old items with new ones
            #         Competition.objects.bulk_create()

            return HttpResponseRedirect('/profile/')
        else:
            return render(request, 'application/student_application.html', {
                'user': request.user,
                # Student Profile Forms
                'profileFormHeader': profileFormHeader,
                'profileFormHeaderSide': profileFormHeaderSide,
                'profileFormSide': profileFormSide,
                'profileFormMain': profileFormMain,
                # Many to Many Formsets
                'languageFormset': languageFormset,
                'competitionFormset': competitionFormset,
                'internshipFormset': internshipFormset,
                'courseworkFormset': courseworkFormset,
                # 'awardFormset': awardFormset,
                # Formset Helper
                'languageFormset_helper': LanguageFormset_helper,
                'internshipFormset_helper': InternshipFormset_helper(),
                'competitionFormset_helper': CompetitionFormset_helper,
                'courseworkFormset_helper': CourseworkFormset_helper,
                # 'awardFormset_helper': AwardFormset_helper(),
            })


@transaction.atomic
def team_registration(request):
    """Display Registration Form for Team Registration"""
    if request.method == "POST": 
        userForm = TeamMemberRegistration(request.POST)
        teamForm = TeamRegistrationForm(request.POST)
        contactForm = ContactForm(request.POST)

        if (userForm.is_valid() and teamForm.is_valid() ):
            team = teamForm.save()
            userForm.team = team
            userForm.save()

            return HttpResponseRedirect('portal:index')
    else:
        userForm = TeamMemberRegistration()
        teamForm = TeamRegistrationForm()
        contactForm = ContactForm()

    return render(request, 'application/team_application.html', {
        'teamForm': teamForm, 
        'userForm': userForm,
        'contactForm': contactForm, 

    })


#-------Application Display--------
from .models import Application

# The Overview Index for the Assessors
# This describes the process and ofers management Views
def review_overview(request):
    # Create a list of all teams to be reviewed by the person
    team_applications = Application.objects.filter(applicant__role='team')
    # Subset list to all teams that have not yet been reviewed
    # Subset list to all teams that already have been reviewed
    return render(request, 'review/review_index.html', {
        'team_applications': team_applications,
    })



def assess_teams(request, slug=None):
    teamlist = Application.objects.filter(applicant__role='team')
    # if teamslug:
    #     team = get_object_or_404(Application, applicant__role='team', slug=teamslug)
    # else:
    team = teamlist[0]

    if request.method=="POST":
        member_assessment_form = MemberReviewForm(request.POST)
        if member_assessment_form.is_valid():
            member_assessment_form.save()
        else:
            return render(request, 'review/teamreview_scoresheet.html', {
                'teamlist': teamlist, 
                'team': team, 
                'member_assessment_form': member_assessment_form,
            })

    member_assessment_form = MemberReviewForm()
    return render(request, 'review/teamreview_scoresheet.html', {
        'team': team,
    })

def expert_applicationlist(request):
    """Displays the list of all applications. Filtering by status"""
    applicationlist = Application.objects.all()
    return render(request, 'application/application_list.html', {
        'applicationlist': applicationlist,
    })

def team_applicationlist(request):
    """Displays the list of all applications. Filtering by status"""
    applicationlist = Application.objects.all()
    return render(request, 'application/application_list.html', {
        'applicationlist': applicationlist,
    })

def application_by(request, role):
    """Displays the list of all applications for a specific Role.
    Meant to be a 'filteredList_View'"""
    applicationlist = Application.objects.filter(applicant__role=role)
    return render(request, 'application/application_byRole.html', {
        'applicationlist': applicationlist,
    })

def application_detail(request,username):
    """Detail View on a single Application"""
    application = Application.objects.filter(applicant__user__username=username)
    return render(request, 'application/application_detail.html', {
        'application': application,
    })

# ----------Process Management ----------------------
def process_overview(request):
    """Managerial Overview displaying the current state of the Review
    process, the associated Assessors and information on the kind and"""
    return render(request, 'review/process_overview', {})

def assessors_overview(request):
    """Assignment and Managing view for the Expert Assessors"""
    return render(request, 'review/assessors_overview.html', {})

def assessors_detail(request):
    """Managerial Detail View on the status, progress and returned review for
    each Expert Assessor."""
    return render(request, 'review/assessors_detail.html', {})

