# General Imports
from django.conf import settings
from django.shortcuts import (render, get_object_or_404, get_list_or_404)
from django.db.models import Q
from datetime import timedelta, date, datetime

# Modelimports
from UserManagement.models import Attendent, Team
from SessionManagement.models import Session, Venue, Shift
from ApplicationManagement.models import Application

# FORM Imports ------
from .forms import ExpertCommentForm, TeamCommentForm

from django.views import View
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Helper Function



# Create your views here.
class DashboardIndex(ListView):
    model = Session
    template_name = 'dashboard/dashboard_index.html'


def expert_management(request, username=None):
    """
    The Interactive administrative Overview over the status and details for all
    Expert Applications with CDRC for the current Year. 
    Control Flows are integrated to allow direct interaction with the Applications
    from initial screening to final invitation/decline decissions.
    """
    expertlist = Application.objects.filter(applicant__role="expert", competition_year='2017')
    expertlist_accepted = Application.objects.filter(Q(status="2") | Q(status="3"), applicant__role="expert", competition_year='2017')
    expertlist_reviewed = Application.objects.filter(status="1", applicant__role="expert", competition_year='2017')
    expertlist_unreviewed = Application.objects.filter(status="0", applicant__role="expert", competition_year='2017')
    expertlist_declined = expertlist.filter(status="4", applicant__role="expert", competition_year='2017')
    if username:
        expert = Application.objects.get(applicant__user__username=username, competition_year='2017')
    else:
        expert = expertlist[0]

    if request.method == "POST":
        form = ExpertCommentForm(request.POST)
        if form.is_valid():
            expert.comments = form.cleaned_data['comment']
            expert.applicant.blacklisted = form.cleaned_data['blacklisted']
            expert.status = form.cleaned_data['status']
            expert.save()
        else:
            return render(request, 'dashboard/expert_mangement.html',{ 
            'expertlist': expertlist,
            'expertlist_unreviewed': expertlist_unreviewed,
            'expertlist_reviewed': expertlist_reviewed,
            'expertlist_accepted': expertlist_accepted,
            'expertlist_declined': expertlist_declined, 
            'expert':expert, 
            'form': form,
            })

    form = ExpertCommentForm(initial={'comment':expert.comments, 
                                'blacklisted':expert.applicant.blacklisted,
                                'status':expert.status})

    return render(request, 'dashboard/expert_management.html', {
        'expertlist': expertlist,
        'expertlist_unreviewed': expertlist_unreviewed,
        'expertlist_reviewed': expertlist_reviewed,
        'expertlist_accepted': expertlist_accepted,
        'expertlist_declined': expertlist_declined, 
        'expert':expert, 
        'form': form,
    })

def team_management(request, slug=None):
    teamlist = Application.objects.filter(applicant__role='team')
    teamlist_unreviewed = Application.objects.filter(status="0", applicant__role='team')
    teamlist_reviewed = Application.objects.filter(status="1", applicant__role="team")
    teamlist_accepted = Application.objects.filter(Q(status="2") | Q(status="3"), applicant__role='team')
    teamlist_declined = Application.objects.filter(status=4, applicant__role='team')
    if slug:
        team = Application.objects.get(applicant__team__slug=slug, competition_year='2017')
    else:
        team = teamlist[0]
    
    # Handle Comment Form
    if request.method=="POST":
        form = TeamCommentForm(request.POST)
        if form.is_valid():
            team.comments = form.cleaned_data['comment']
            team.status = form.cleaned_data['status']
            team.save()
        else:
            return render(request, 'dashboard/team_management.html', {
                'teamlist': teamlist,
                'teamlist_unreviewed': teamlist_unreviewed,
                'teamlist_reviewed': teamlist_reviewed,
                'teamlist_accepted': teamlist_accepted,
                'teamlist_declined': teamlist_declined, 
                'team': team,
                'form': form,
            })

    form = TeamCommentForm(initial={'comment': team.comments, 'status':team.status})
    return render(request, 'dashboard/team_management.html', {
        'teamlist': teamlist,
        'teamlist_unreviewed': teamlist_unreviewed,
        'teamlist_reviewed': teamlist_reviewed,
        'teamlist_accepted': teamlist_accepted,
        'teamlist_declined': teamlist_declined, 
        'team': team,
        'form': form, 
    })

class SessionManagement(ListView):
    model = Session

    def get(self, request, slug=None):
        if slug:
            selected_session = Session.objects.get(slug=slug)
        else:
            selected_session = Session.objects.all()[0]
        
        # Information on the 
        context = {
            'session_list' : Session.objects.all().order_by('-startTime'),
            'selected_session': selected_session,
        }
        return render(request, 'dashboard/session_management.html',context)



class VenueManagement(DetailView):
    model = Venue

    START_DATE = datetime(2017, 8, 5)
    END_DATE = datetime(2017, 8, 12)
    def daterange(start_date, end_date):
            """
            Returns a generator object to be used for the construction of 
            planning tables to manage Time Availabilities.
            """
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

    def get(self, request, slug=None):
        if slug:
            selected_venue = Venue.objects.get(slug=slug)
        else:
            selected_venue = Venue.objects.all()[0]

        # Information on the selected Venue
        rooms_sel = selected_venue.room_set.all()
        session_sel = selected_venue.session_set.all()

        context = {
            'venue_list': Venue.objects.all(),
            'selected_venue': selected_venue,
            'session_sel': session_sel,
            'rooms_sel': rooms_sel,
            'competition_days' : [day for day in settings.CONVENTION_DAYS],
        }
        return render(request, 'dashboard/venue_management.html', context)


class ShiftManagement(ListView):
    model = Session
    template_name = 'dashboard/shift_management.html'
