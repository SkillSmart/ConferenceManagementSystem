from django.shortcuts import render, HttpResponsePermanentRedirect
from django.urls import reverse
from .forms import (SessionModelForm, SessionCreateForm, SessionEditForm)
from .models import Session
# CBGV Imports
from django.views.generic.edit import (CreateView, DeleteView, UpdateView)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.
class SessionCreateView(CreateView):
    model = Session
    form_class = SessionCreateForm
    template_name = 'session/forms/sessionCreate_form.html'
    # success_url = reverse('session:session_list')

class SessionDetailView(DetailView):
    model = Session
    template_name = 'session/session_detail.html'

class SessionListView(ListView):
    model = Session
    template_name = 'session/session_list.html'

class SessionEditView(UpdateView):
    model = Session
    template_name = 'session/forms/sessionEdit_form.html'
    form_class = SessionEditForm
    success_url = ('/sessions/')



