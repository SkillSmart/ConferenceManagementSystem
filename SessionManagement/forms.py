from django import forms
from .models import (Venue, Room)
from .models import (Session, Availability, Shift)

# Define the Forms here. 
class SessionModelForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = []

class SessionCreateForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = []

class SessionEditForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = []


class VenueCreateForm(forms.ModelForm):
    class Meta:
        model = Venue
        exclude = []