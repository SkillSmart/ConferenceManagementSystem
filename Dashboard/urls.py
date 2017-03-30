from django.conf.urls import url

# View Imports
from . import views

app_name = "dashboard"

urlpatterns = [
    url(r'^$', views.management_index, name='index'),
    url(r'^experts/$', views.expert_management, name='manage_experts'),
    url(r'^experts/(?P<username>.+)/$', views.expert_management, name="expert_detail"),
    url(r'^sessions/$', views.session_management, name="manage_sessions"),
    url(r'^teams/$', views.team_management, name='manage_teams'),
    url(r'^teams/(?P<slug>.+)/$', views.team_management, name='team_detail'),
    url(r'^venues/$', views.venue_management, name='manage_venues'),
    url(r'^shifts/$', views.shift_management, name='manage_shifts'),
]
