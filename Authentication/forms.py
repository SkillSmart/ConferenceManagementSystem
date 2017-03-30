from django import forms
from django.contrib.auth.models import User
from UserManagement.models import Attendent

# --- Entitiy Management Forms ------
class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields=['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self):
        if (self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password')):
            raise ValidationError("Password does not match.")
        return self.cleaned_data

class AttendentModelForm(forms.ModelForm):
    class Meta:
        model = Attendent
        exclude = []

# ---- Authentication Action Forms ---------
class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput())
    newPassword = forms.CharField(widget=forms.PasswordInput())
    newPassword_repeat = forms.CharField(widget=forms.PasswordInput())



    def clean(self):
        if( self.cleaned_data['newPassword'] != self.cleaned_data['newPassword_repeat']):
            raise ValidationError("The new Passwords given do not match.")
        return cleaned_data
# ---- Profile Edit Forms -------
class UserAccountForm(UserModelForm):
    exclude = ['password', 'confirm_password']

