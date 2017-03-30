import requests
from django.db import models
from django.urls import reverse_lazy
from UserManagement.models import Attendent, ExpertProfile, Team
# Import for Google Maps Plugin
from django_google_maps import fields as map_fields
from django.utils.text import slugify
# --------------Location Management -------------------
from datetime import datetime


# Define general helper Functions
def geocode(lat, lng):
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor=false".format(
        lat=lat,
        lon=lng
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    return response.json()['results'][0]['formatted_address']


class Venue(models.Model):
    """A specific location that houses rooms where Sessions take place."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    img_venue = models.ImageField(upload_to="venues/locationImg/", blank=True)
    # Google Maps Plugin - LocationInformation
    map_img = models.FileField(upload_to='venues/locationMap/', blank=True)
    address = map_fields.AddressField(max_length=200, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, null=True)
    
    directions = models.TextField(max_length=350, null=True)
    location_info = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('portal:venue_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.address = geocode(self.geolocation.lat, self.geolocation.lon)
        super().save(*args, **kwargs)
        

    
    
class Room(models.Model):
    """A specific Room available to be assigned to a session."""
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=60)
    # Comment section for information as to equipment and specials
    directions = models.TextField(max_length=2000, null=True)
    level = models.CharField(max_length=50, null=True)
    notes = models.TextField(blank=True, null=True)    
    # Display information
    img_presentation = models.ImageField(upload_to="venues/presentationImg/", blank=True)
    
    # Management related hidden fields
    _internal_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
# -----  STATE MODELS ----------
class Availability(models.Model):
    """
    A continous stretch of available time for a given Room
    to be used with a Session.
    """
    Room = models.ForeignKey(Room)
    free_from = models.DateTimeField()
    free_till = models.DateTimeField()

    # Calculate amount of time available in this stretch
    
    
    def schedule(self, session):
        """
        Checks if the Time associated with the Session planned fits
        within the given availability. Returns Boolean answer.
        """
        return True

    def duration(self):
        duration = self.free_from - self.free_till
        return duration 
    
    def get_gps_location(self):
        pass
        
    def __str__(self):
        return "{}: {}".format(self.free_from, self.duration)
    # TODO: Turn the location ino GPS for displaying on a map

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# ---------------Session Management-----------------------
class Session(models.Model):
    """A specific Round of Mediation between two Negotiating Teams and a Mediator
    scheduled for a given Date and Time in a room at a certain Venue."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    # The Teams taking part
    mediatorTeam = models.ForeignKey(Team, related_name="mediatorteam")
    negotiatorTeam = models.ForeignKey(Team, related_name="negotiatorteam")

    # The Assessors taking part
    assessors = models.ManyToManyField(ExpertProfile)

    # The Room scheduled
    room = models.ForeignKey(Room)
    # The Timeslot scheduled
    startTime = models.DateTimeField(blank=True, null=True)
    endTime = models.DateTimeField(blank=True, null=True)
    # Additional Ressources Scheduled
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('session:session_detail', args=[self.slug])

# ----------------Work Management-------------------------
class Shift(models.Model):
    """A flexible amount of time a given Person is available for Work at the Comp."""
    staff = models.ForeignKey(Attendent)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return "{} to {}".format(self.start, self.end)
