from django.conf.urls import url

# View Imports
from . import views

app_name = "dashboard"

urlpatterns = [
    url(r'^$', views.DashboardIndex.as_view(), name='index'),
    # Set of Dashboard Views to control the other modules
    url(r'^settings/$', views.DashboardSettings.as_view(), name='index_settings'),
    url(r'^settings/expert_application/$', views.DashboardExpert.as_view(), name='index_expert'),
    url(r'^settings/team_application/$', views.DashboardTeam.as_view(), name='index_team'),
    url(r'^settings/venue_management/$', views.DashboardVenue.as_view(), name='index_venue'),
    url(r'^settings/session_management/$', views.DashboardSession.as_view(), name='index_session'),
    url(r'^settings/shift_management/$', views.DashboardShift.as_view(), name='index_shift'),
    # The Dashboard Module Views
    url(r'^experts/$', views.expert_management, name='manage_experts'),
    url(r'^experts/(?P<username>.+)/$', views.expert_management, name="expert_detail"),
    url(r'^sessions/$', views.SessionManagement.as_view(), name="manage_sessions"),
    url(r'^teams/$', views.applicationoverview_team, name='manage_teams'),
    url(r'^teams/(?P<slug>[-\w]+)/$', views.team_management, name='team_detail'),
    url(r'^venues/$', views.VenueManagement.as_view(), name='manage_venues'),
    url(r'^venues/(?P<slug>[-\w]+)/$', views.VenueManagement.as_view(), name='manage_venue_detail'),
    url(r'^shifts/$', views.ShiftManagement.as_view(), name='manage_shifts'),
    # Accept and Decline Applications directly
    url(r'^accept/(?P<pk>\d+)/$', views.accept_application, name='accept_application'),
    url(r'^decline/(?P<pk>\d+)/$', views.decline_application, name='decline_application'),
    url(r'^test/$', views.test_model, name='test'),
]
