from django.conf.urls import url
from . import views as application_views

app_name = 'application'

# Application Registration Process
urlpatterns = [
    url(r'^$', application_views.user_registration, name='register_user'),
    url(r'^team/$', application_views.team_registration, name='register_team'),
    url(r'^student/$', application_views.student_registration, name='register_student'),
    url(r'^expert/$', application_views.expert_registration, name='register_expert'),
]

# Application Management Views
urlpatterns += [
    url(r'^review/$', application_views.review_overview, name='review_index'),
    url(r'^review/teams/(?P<slug>[-\w]+)/$', application_views.assess_teams, name='review_index'),
    url(r'^review/teams/', application_views.assess_teams, name='team_overview'),
    # url(r'^team/detail/(?P<role>\w+/$)', application_views.application_by, name='role_overview'),
    # url(r'^()', application_views.application_judgeOverview, name='')
]

# # Review/Assessment Views
# urlpatterns = [
# ]