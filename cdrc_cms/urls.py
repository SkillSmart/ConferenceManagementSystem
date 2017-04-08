"""cdrc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from cdrc_cms import settings

# This is added to get the traditional views
from django.contrib.auth import views as auth_views
from Authentication import views as authentication_views
from ApplicationManagement.views import AccountRegistrationView

# Application INCLUDES
urlpatterns = [
    url(r'^', include('Portal.urls')),
    url(r'^application/', include('ApplicationManagement.urls')),
    url(r'^profile/', include('UserManagement.urls')),
    url(r'^sessions/', include('SessionManagement.urls')),
    url(r'^dashboard/', include('Dashboard.urls')),
]

# AUTHENTICATION
urlpatterns += [
    url(r'^login/', authentication_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', authentication_views.LogoutView.as_view(), name='logout'),
    url(r'^change-password/$', auth_views.password_change, 
    {'template_name': 'authentication/changePassword.html'}),
    url(r'^reset-password/$', auth_views.password_reset, {
        'template_name':'authentication/resetPassword.html'
    }, name='password_reset'),
    url(r'^reset-password-done/$', auth_views.password_reset_done, {
        'template_name': 'authentication/resetPasswordDone.html'}, name="password_reset_done"),
    url(r'^admin/', admin.site.urls),
] 
# Additon to serve Media when DEBUG=TRUE

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)