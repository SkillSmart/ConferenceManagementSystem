from django.shortcuts import render
from UserManagement.models import (Student, Expert, Team, TeamProfile, 
                                    StudentProfile, ExpertProfile)
from UserManagement.models import (MediationExperience, NegotiationExperience, 
                                    Course)
from SessionManagement.models import (Venue, Room, Session)
from django.contrib.auth.models import User

# Utils import
from django.db.models import Q, F
# CBGV Imports
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# CBGV Mixins
from django.views.generic.edit import FormMixin

# FORMS:::
from .forms import ExpertSearchForm, TeamSearchForm, TeamEditForm
# from .forms import TeamEditForm
from SessionManagement.forms import (VenueCreateForm)

# Create your views here.
class IndexView(ListView):
    model = Student
    template_name = 'portal/index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['experts_invited'] = Expert.objects.all()
        context['teams_invited'] = Team.objects.all()
        context['venues'] = Venue.objects.all()
 
        return context

class CompetitionIndex(ListView):
    template_name = 'portal/competition/competition_index.html'
    model = Session

    def get_context_data(self):
        context = super(CompetitionIndex, self).get_context_data()
        context['sessionList_current'] = Session.objects.all()
        context['sessionList_upcoming'] = Session.objects.all()
        context['todays_venues'] = Venue.objects.all()
        context['todays_teams'] = Team.objects.all()
        return context


#  -------- VENUE Section --------------
class VenueIndex(ListView):
    model = Venue
    template_name = 'portal/venues/venue_index.html'

class VenueManagementView(ListView):
    model = Venue
    template_name = 'portal/venues/venue_list.html'

class VenueCreate(CreateView):
    model = Venue
    form_class = VenueCreateForm
    template_name = 'session/forms/venueCreate_form.html'

class VenueDetailView(DetailView):
    model = Venue
    template_name = 'portal/venues/venue_detailview.html'
    context_object_name = 'location'

    def get_context_data(self, object):
        context = super(VenueDetailView, self).get_context_data()
        context['geolocation'] = object.geolocation
        return context

# ---- TEAMS Section ---------
class TeamListView(FormMixin, ListView):
    model = Team
    form_class = TeamSearchForm
    template_name = 'portal/teams/team_listview.html'

class TeamDetailView(DetailView):
    model = Team
    template_name = 'portal/teams/team_detailview.html'

class TeamEditView(UpdateView):
    model = Team
    template_name = 'portal/teams/team_editview.html'
    form_class = TeamEditForm

# --- EXPERTS Section --------
class ExpertListView(ListView):
    model = Expert
    context_object_name = 'expert_list'
    template_name = 'portal/experts/expert_list.html'

    def get_context_data(self):
        context = super(ExpertListView, self).get_context_data()
        context['medExp_list'] = MediationExperience.ROLES
        context['negExp_list'] = NegotiationExperience.ROLES
        context['search_form'] = ExpertSearchForm()
        return context

class ExpertDetailView(DetailView):
    model = ExpertProfile
    context_object_name = 'expert'
    template_name = 'portal/experts/expert_detail.html'
    slug_field = 'user__username'


#  ---- STUDENT Section ----------
class StudentListView(ListView):
    model = StudentProfile
    template_name = 'portal/students/student_list.html'
    context_object_name = 'student_list'


class StudentDetailView(DetailView):
    model = StudentProfile
    slug_field = 'user__username'
    template_name = 'portal/students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, object):
        context = super(StudentDetailView, self).get_context_data()
        context['negotiationCourses'] = Course.objects.filter(subject='negotiation')
        context['mediationCourses'] = Course.objects.filter(subject='mediation')
        return context