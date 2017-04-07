from django.contrib import admin
from . import models

# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'selection_status', 'review_status', 'term_accepted', 'comments']
    list_filter = ['selection_status', 'term_accepted']
    search_fields = ['applicant', 'status', 'comments']

class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'selection_status', 'review_status', 'term_accepted', 'comments']
    list_filter = ['selection_status', 'term_accepted']
    search_fields = ['applicant', 'status', 'comments']
admin.site.register(models.StudentApplication, StudentApplicationAdmin)

class TeamApplicationAdmin(admin.ModelAdmin):
    list_display = []
admin.site.register(models.TeamApplication, TeamApplicationAdmin)

class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = []
admin.site.register(models.StaffApplication, StaffApplicationAdmin)


# Application Related Models
admin.site.register(models.Review)
admin.site.register(models.Feedback)