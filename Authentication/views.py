from django.conf import settings
# Auth functions
from django.contrib.auth import logout, login, authenticate, views
# Helper
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from .forms import UserModelForm, LoginForm

# Import Class based Views
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.
def index(request):
    return render(request, 'authentication/index.html', {})

class LoginView(FormView):
    """ Login Form posts here """
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        super(LoginView, self).form_valid(form)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email = form.cleaned_date)
        if user:
            login(request, request.user)
        else:
            return render(request, 'authentication/login.html', {
                'form': form,
            })

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class SignupView(View):
    template_name = 'authentication/signup.html'
    form_class = UserModelForm
    success_url = '/application/'

    # Helper Methods for Form handling
    def check_valid(self, *args):
        for form in args:
            if not form.is_valid():
                return False
            return True

    def forward_next(self, role):
        """Determines the logic where to forward based on the role chosen"""
        if role in settings.STUDENT_ROLES:
            return '/application/student'
        if role in settings.EXPERT_ROLES:
            return'/application/expert/'
        if role in settings.STAFF_ROLES:
            return '/application/staff/'
        if role == "team":
            return '/application/team/'
        else:
            return HttpResponseRedirect('/')
    # Handling the HttpRequest Types
    def get(self, request):
        # Instantiate the forms
        user_form = UserModelForm()
        attendent_form = AttendentModelForm()

        return render(request, 'authentication/signup.html', {
            'user_form': user_form,
            'attendent_form': attendent_form,
        })

    def post(self, request, role):
        user_form = UserModelForm(request.POST)
        attendent_form = AttendentModelForm(request.POST)

        if self.check_valid(user_form, attendent_form):
            # Create user object and add the username to it
            user = user_form.save(commit=False)
            user.username = "{}.{}".format(user.first_name, user.last_name)
            user.save()
            # Save the attendent form for the user created
            attendent = attendent_form.save(commit=False)
            attendent.user = user
            attendent.save()

            # Loging the person into the system and continuing to profile creation
            login(request, user)
            # Then finally redirect to the appropriate place
            return HttpResponseRedirect(self.forward_next('expert'))
        else:
            return render(request, 'authentication/signup.html', {
                'user_form': user_form, 
                'attendent_form': attendent_form,
            })

def change_password(request):
    template_response = views.password_change(request)
    # Do something with 'template_response'
    return template_response

# def logout(request):
#     logout(request)
#     return HttpResponseRedirect('/')