from django.conf.urls import url
from . import views 


app_name = "session"

urlpatterns = [
    url(r'^$', views.SessionListView.as_view(), name='overview'),
    url(r'^create/$', views.SessionCreateView.as_view(), name='session_create'),
    url(r'^(?P<slug>[\w\-]+)/$', views.SessionDetailView.as_view(), name="session_detail"),
    url(r'^(?P<slug>[\w\-]+)/edit/$', views.SessionEditView.as_view(), name="session_edit"),
]