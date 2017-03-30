from django.contrib import admin
from . import models
# Import for Google Maps Plugin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

# Location Management

class VenueAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
admin.site.register(models.Venue, VenueAdmin)
admin.site.register(models.Room)

# Session related Staff Management
admin.site.register(models.Session)


