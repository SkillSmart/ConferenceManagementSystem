from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings

# MODEL Imports ---------
from ApplicationManagement.models import Application

# FORM Imput -----------
from .forms import ContactForm
from .forms import UserRegistrationForm, TeamRegistrationForm
from .forms import TeamMemberRegistration
from .forms import TeamRegistrationForm
# ----Student Forms-------------
from .forms import StdProfileForm_head, StdProfileForm_main, StdProfileForm_side 
from .forms import LanguageFormset, InternshipFormset, CompetitionFormset, CourseworkFormset, AwardsFormset
from .forms import LanguageFormset_helper, InternshipFormset_helper, CompetitionFormset_helper, CourseworkFormset_helper, AwardsFormset_helper
# ---ExpertForms-------------
from .forms import ExpertProfileFormHeader, ExpertProfileFormMain, ExpertProfileFormSide, ExpertProfileForm
from .forms import MediationExperienceFormset, NegotiationExperienceFormset
from .forms import MediationExperienceFormset_helper, NegotiationExperienceFormset_helper
# ---ASSESSMENT Forms -------
from .forms import MemberReviewForm

# General Informa



# ------Application Process Forms ---------
def user_registration(request):
    return render(request, 'application/registration.html', {
    })

def expert_registration(request):
    """Display the Registration Form for the User Registration Process"""
    if request.method =="POST":
        userForm = UserRegistrationForm(request.POST)
        profileFormHeader = ExpertProfileFormHeader(request.POST)
        profileFormSide = ExpertProfileFormSide(request.POST)
        profileFormMain = ExpertProfileFormMain(request.POST)
        mediationExp = MediationExperienceFormset(request.POST)
        negotiationExp = NegotiationExperienceFormset(request.POST)
        
        if (userForm.is_valid() and profileFormHeader.is_valid() and profileFormMain.is_valid() and profileFormSide.is_valid()
            and mediationExp.is_valid() and negotiationExp.is_valid()):
            userForm.save()
            ExpertProfileForm(profileFormHeader.cleaned_data, profileFormMain.cleaned_data, profileFormSide.cleaned_data).save()
           

            return HttpResponseRedirect('portal:index')
        else:
            userForm = UserRegistrationForm(request.POST)
            profileFormHeader = ExpertProfileFormHeader(request.POST)
            profileFormSide = ExpertProfileFormSide(request.POST)
            profileFormMain = ExpertProfileFormMain(request.POST)
            mediationExp = MediationExperienceFormset(request.POST)
            negotiationExp = NegotiationExperienceFormset(request.POST)

    else:
        userForm = UserRegistrationForm()
        profileFormHeader = ExpertProfileFormHeader()
        profileFormSide = ExpertProfileFormSide()
        profileFormMain = ExpertProfileFormMain()
        mediationExp = MediationExperienceFormset()
        negotiationExp = NegotiationExperienceFormset()

    return render(request, 'application/expert_application.html', {
        'user': request.user,
        'userForm': userForm, 
        'profileFormHeader': profileFormHeader,
        'profileFormSide': profileFormSide,
        'profileFormMain': profileFormMain,
        'mediationExp': mediationExp,
        'mediationExp_helper': MediationExperienceFormset_helper(),
        'negotiationExp': negotiationExp, 
        'negotiationExp_helper': NegotiationExperienceFormset_helper(),
    })

@login_required
@transaction.atomic
def student_registration(request):
    """Display the Registration Form for the User Registration Process"""
    if request.method =="POST":
        userForm = UserRegistrationForm(request.POST)
        profileFormHeader = StdProfileForm_head(request.POST)
        profileFormSide = StdProfileForm_side(request.POST)
        profileFormMain = StdProfileForm_main(request.POST)
        internshipFormset = InternshipFormset(request.POST)
        competitionFormset = CompetitionFormset(request.POST)
        courseworkFormset = CourseworkFormset(request.POST)
        languageFormset = LanguageFormset(request.POST)
        awardsFormset = AwardsFormset(request.POST)
       
        if (userForm.is_valid()):
            # Create User
            user = userForm.save(commit=False)
            if user.cleaned_data.get['password_set'] == user.cleaned_data.get['password_repeat']:
                user.set_password(userForm.cleaned_data.get['password_set'])
                user.save()
            else:
                raise ValidationError('Your passwords do not match')
            profileForm.save(commit=False)
            # Add additional Information to profileForm
            profile = profileForm.save(commit=False)
            profile.team = request.user.attendent.team
            profile.save()
            
            # Save Formsets
            intExpFormset.instance = user
            intExpFormset.save()

            competitionFormset.instance = user
            competitionFormset.save()

            courseworkFormset.instance = user
            courseworkFormset.save()

            return HttpResponseRedirect('portal:index')

    else:
        userForm = UserRegistrationForm(instance=request.user)
        profileFormHeader = StdProfileForm_head()
        profileFormSide = StdProfileForm_side()
        profileFormMain = StdProfileForm_main()
        languageFormset = LanguageFormset()
        internshipFormset = InternshipFormset()
        competitionFormset = CompetitionFormset()
        courseworkFormset = CourseworkFormset()
        awardsFormset = AwardsFormset()

    return render(request, 'application/student_application.html', {
        'user': request.user,
        # Forms
        'userForm': userForm, 
        'profileFormHeader': profileFormHeader,
        'profileFormSide': profileFormSide,
        'profileFormMain': profileFormMain,
        'languageFormset': languageFormset,
        'competitionFormset': competitionFormset,
        'internshipFormset': internshipFormset,
        'courseworkFormset': courseworkFormset,
        'awardsFormset': awardsFormset,
        'languageFormset_helper': LanguageFormset_helper(),
        'internshipFormset_helper': InternshipFormset_helper(),
        'competitionFormset_helper': CompetitionFormset_helper(),
        'courseworkFormset_helper': CourseworkFormset_helper(),
        'awardsFormset_helper': AwardsFormset_helper(),
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

def assess_team(request, teamslug=None):
    teamlist = get_list_or_404(Application, applicant__role='team')
    if teamslug:
        team = get_object_or_404(Application, role='team', slug=teamslug)
    else:
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

