from django.shortcuts import render, HttpResponseRedirect
from .models import Attendent
# Class Imports
from .models import ExpertProfile, TeamProfile, StudentProfile
from .models import Program
# Form Imports
from .forms import ExpertModelForm, TeamModelForm, UserProfileForm, UserModelForm, StudentModelForm
from .forms import NegotiationExperienceForm, MediationExperienceForm
from .forms import MediationExperienceFormset, MediationExperienceFormset_helper, NegotiationExperienceFormset, NegotiationExperienceFormset_helper
from .forms import ProgramFormSet, ProgramFormSet_helper
# Student Forms
from .forms import InternshipForm, CourseForm, AwardForm

# Switch Statements for the different Forms to be used 

# Replace with inline Form Generated Formlist 
member_forms = [
    StudentModelForm()
    ]

PROFILE_FORM = {
    'expert': ExpertModelForm,
    'mediator': member_forms,
    'negotiator': member_forms,
    'coach': ExpertModelForm,
    'staff': StudentProfile,
    }
MEDEXP_FORM = {
    'expert': MediationExperienceForm,
    'coach': MediationExperienceForm,
    'mediator': InternshipForm,
    'negotiator': InternshipForm,
    'staff': None,
}
NEGEXP_FORM = {
    'expert': NegotiationExperienceForm,
    'coach': NegotiationExperienceForm,
    'mediator': InternshipForm,
    'negotiator': InternshipForm,
    'staff': None,
}
# ----- Profile Creation ----------
def profile_create(request):
    
    # When Student Team application is selected       
    if request.method=="POST":
        profile_form = PROFILE_FORM[request.user.attendent.role](request.POST)
        negExp_form = NEGEXP_FORM[request.user.attendent.role](request.POST)
        medExp_form = MEDEXP_FORM[request.user.attendent.role](request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.attendent = request.user.attendent
            profile.save()

        if negExp_form.is_valid():
            negExp_form.save()

        if medExp_form.is_valid():
            medExp_form.save()

    else:
        profile_form = PROFILE_FORM[request.user.attendent.role]
        negExp_form = NEGEXP_FORM[request.user.attendent.role]
        medExp_form = MEDEXP_FORM[request.user.attendent.role]

    return render(request, 'registration/profile_create.html', {
        'attendent': Attendent.objects.get(user = request.user),
        'profile_form': profile_form,
        'members': member_forms,
        'negExp_form': negExp_form,
        'medExp_form': medExp_form,
    })

# --- Profile Management ---------
def profile_delete(request):
    if request.method=="POST":
        if request.delete:
            pass

    return render(request, 'profile/profile_delete.html', {})

def profile_display(request):
    # Switch Dicctionary to display the right form    
    return render(request, 'portal/experts/experts_detailview.html', {
        'expert': ExpertProfile.objects.get(user=request.user)
    })

def profile_edit(request):

    if request.method == "POST":
        userForm = UserProfileForm(request.POST, request.FILES, instance=request.user)
        expertForm = ExpertModelForm(request.POST, request.FILES, instance=request.user.profile.expertprofile)
        mediationFormSet = MediationExperienceFormset(request.POST)

        if (userForm.is_valid() and expertForm.is_valid() and mediationFormSet.is_valid()):
            user = userForm.save()
            expertForm.save()

            mediationFormSet.object = user
            mediationFormSet.save()

            return HttpResponseRedirect('/profile')

        else:
            return render(request, 'profile/profile_edit.html', {
                'userForm': userForm,
                'expertForm': expertForm,
            })

    userForm = UserProfileForm(instance=request.user)
    expertForm = ExpertModelForm(instance=request.user.profile.expertprofile)

    return render(request, 'profile/profile_edit.html', {
        'userForm': userForm,
        'expertForm': expertForm,
        'programFormSet': ProgramFormSet(instance=request.user.profile.expertprofile),
        'programFormSetHelper': ProgramFormSet_helper(),
        'mediationFormSet': MediationExperienceFormset(instance=request.user.profile.expertprofile),
        'mediationFormSetHelper': MediationExperienceFormset_helper(),
        'negotiationFormSet': NegotiationExperienceFormset(instance=request.user.profile.expertprofile),
        'negotiationFormSetHelper': NegotiationExperienceFormset_helper(),
        })


# ------ Profile Interaction -----------

# TESTCASE
def profile_test(request):
    if request.method == "POST":
        form = ExpertModelForm(request.POST, request.FILES, instance=request.user.profile.expertprofile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile')
    profileForm = ExpertModelForm(instance=request.user.profile.expertprofile)
    return render(request, 'profile/test.html', {
        'profileForm': profileForm,
        })


# -------------- SCORING VIEWS ----------------------
"""
Related CRUD views to Scoring of Teams trough Expert Panels and Experts trough the 
respective Students. All information is adminstered trough visual uncluttered interfaces.
The Users will have only this clearance to work with, so a direct entry is needed.
"""
from django.views.generic import CreateView, ListView, DetailView, DeleteView

# ---- EXPERT Scoresheet ------------
def score_expert(CreateView):
    return render(request, 'scoring/expert_scoresheet.html', {})

def result_expert(CreateView):
    return render(request, 'scoring/expert_result.html', {})


# ---- SESSION Scoresheet ----------------
def score_session(request):
    return render(request, 'scoring/session_scoresheet.html', {})

def result_session(CreateView):
    return render(request, 'scoring/session_result.html', {})

# ---- TEAM Scoresheet -------------------

