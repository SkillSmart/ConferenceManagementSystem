from django.conf.urls import url
from . import views as profile_views

app_name = 'userManagement'

urlpatterns = [
    url(r'^$', profile_views.profile_display, name='profile'),
    url(r'create/studentprofile/$', profile_views.StudentProfileCreateView.as_view(), name='create_studentprofile'),
    url(r'create/teamprofile/$', profile_views.TeamProfileCreateView.as_view(), name='create_teamprofile'),
    url(r'create/expertprofile/$', profile_views.ExpertProfileCreateView.as_view(), name='create_expertprofile'),
    url(r'create/staffprofile/$', profile_views.StaffProfileCreateView.as_view(), name='create_staffprofile'),
    url(r'^edit/$', profile_views.profile_edit, name='profile_edit'),
    url(r'^delete/$', profile_views.profile_delete, name='profile_delete'),
    url(r'^test/$', profile_views.profile_test, name="test"),
]
# Profile Registration ulrs
urlpatterns += [
]
# Scoring Related Views
urlpatterns += [
    # url(r'^scores/$', profile_views.score_list, name='scores'),
    # url(r'^scores/(?P<session_slug>.+)/$', profile_views.score_detail, name='sessionScores'),

]