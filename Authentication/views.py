from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import views
from .forms import UserModelForm, AttendentModelForm
from django.contrib.auth import login


# Create your views here.
def index(request):
    return render(request, 'authentication/index.html', {})


def change_password(request):
    template_response = views.password_change(request)
    # Do something with 'template_response'
    return template_response

def signup(request):
    registered = False

    if request.method=="POST":
        account_form = UserModelForm(data=request.POST)
        attendent_form = AttendentModelForm(data=request.POST)
        
        if account_form.is_valid() and attendent_form.is_valid():
            user = account_form.save(commit = False)
            user.username = "{}.{}".format(user.first_name, user.last_name)
            user.set_password(user.password)
            user.save()

            attendent = attendent_form.save(commit=False)
            attendent.user = user
            attendent.save()

            registered=True
            login(request, user)
            return HttpResponseRedirect('/profile/create/')

    else:
        attendent_form = AttendentModelForm()
        account_form = UserModelForm()

    return render(request, 'authentication/signup.html', {
        'attendent_form':attendent_form,
        'account_form':account_form, 
    })

