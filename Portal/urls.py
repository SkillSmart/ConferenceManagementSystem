from django.conf.urls import url, include
from . import views

app_name = 'portal'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^competition/$', views.CompetitionIndex.as_view(), name='competition'),
    url(r'^venue/$', views.VenueIndex.as_view(), name="venues"),
    url(r'^venue/manage/$', views.VenueManagementView.as_view(), name="manage_venue"),
    url(r'^venue/create/$', views.VenueCreate.as_view(), name='create_venue'),
    url(r'^venue/(?P<slug>.+)/', views.VenueDetailView.as_view(), name="venue_detail"),
    url(r'^teams/$', views.TeamListView.as_view(), name='teams'),
    url(r'^teams/(?P<slug>[\w\-]+)/$', views.TeamDetailView.as_view(), name="team_profile"),
    url(r'^teams/(?P<slug>[\w\-]+)/edit/$', views.TeamEditView.as_view(), name="edit_team"),
    url(r'^experts/$', views.ExpertListView.as_view(), name='experts'),
    url(r'^expert/(?P<slug>[\w\.]+)/$', views.ExpertDetailView.as_view(), name='expert_profile'),
    url(r'^students/$', views.StudentListView.as_view(), name="students"),
    url(r'^student/(?P<slug>[\w\.]+)/', views.StudentDetailView.as_view(), name='student_profile'),
    url(r'^session/', include('SessionManagement.urls')),
]