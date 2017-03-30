from django.contrib import admin
from . import models

# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'status', 'term_accepted', 'comments']
    list_filter = ['status', 'term_accepted']
    search_fields = ['applicant', 'status', 'comments']
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Review)
admin.site.register(models.Feedback)