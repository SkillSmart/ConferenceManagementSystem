from datetime import datetime
from django.conf import settings
# General Imports

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Automatic Account Association between User and Attendent Account in Registration
from django.db.models.signals import post_save
from django.dispatch import receiver
# Country Field import
from django_countries.fields import CountryField
# URL resolvers
from django.urls import reverse
# Calculation imports
from django.db.models import (Avg, StdDev, Sum, Max, Min)


PRACTICE_FIELDS = (
        ('negotiation', 'Negotiation'),
        ('mediation', 'Mediation'),
        ('arbitration', 'Arbitratiion')
    )
# -------------------  Roles within the Competition  ------------------

class Attendent(models.Model):
    # META CLASS
    """A Person attending the Competiton. Information stored to keep track
    on Applications before and behaviour during Competition over Time.
    Reused in later application processes."""

    class Meta:
        abstract = True

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blacklisted = models.BooleanField(default=False)
    administrativeComment = models.TextField(blank=True, null=True)

    # Store Information on the Current Year for easy retrieval
    current_application = None

    def get_current_application(self):
        """
        Used to get the current application from inside a template.
        Returns None when no application present.
        """
        application = self.application_set.get(competition_year=settings.START_DATE.year)
        if application:
            return application
        else:
            return None

    def __str__(self):
        return "{}".format(self.user)
    
    def save(self, *args, **kwargs):
        self.current_application = self.application_set.filter(competition_year=settings.START_DATE.year)
        super(Attendent, self).save(*args, **kwargs)


# This automatically creates an Attendent Instance for every User on save
# @receiver(post_save, sender=User)
# def create_attendent_profile(sender, instance, created, **kwargs):
#     if created:
#         Attendent.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_attendent_profile(sender, instance, **kwargs):
#     instance.attendent.save()

class Student(Attendent):
    """
    Can be in role(Mediator, Negotiator)
    """
    role = models.CharField(max_length=35, choices=settings.STUDENT_ROLES)

    # Models Storage related Methods
    def get_absolute_url(self):
        return reverse('portal:student_profile', args = [self.user.username])

    def __init__(self, *args, **kwargs):
        super(Student, self).__init__(*args, **kwargs)
        # Initialize Student instance relevant Information here
    
    # STUDENT SPECIFIC METHODS


class Expert(Attendent):
    """
    Can be in role(Assessor, Rater, CommiteeMember)
    Only Assessors go trough an explicit Application process
    All other roles get created by invitation from the Organizers
    """
    role = models.CharField(max_length=35, choices=settings.EXPERT_ROLES)
    # Expert related Feedback Scores


    # Models Storage related Methods
    def get_absolute_url(self):
        return reverse('portal:expert_profile', args = [self.user.username])

    def __init__(self, *args, **kwargs):
        super(Expert, self).__init__(*args, **kwargs)
        # Initialize necessary starting values for Expert Specific Applications
        availabilities = {}

    def save(self, *args, **kwargs):
        super(Expert, self).save(*args, **kwargs)
    
    # EXPERT SPECIFIC METHODS
    def get_ratings(self, year=datetime.now().year):
        # Catch all given Feedback
        if self.feedback_set.all():
            # Calculate the AVG Values
            return self.feedback_set.filter(date__year=year).aggregate(Avg('feedbackQuality'), Avg('feedbackRelated'), Avg('feedbackComm'))
        else:
            return None

class Team(Attendent):
    """Group of Students applying from a University for the Competition.
    Consisting of individual Team Members and an Associated Coach."""
    role = models.CharField(max_length=35, choices=settings.TEAM_ROLES)
    # Specific Team Values
    university = models.CharField(max_length=100)
    university_logo = models.ImageField(upload_to='team/university_logo/', blank=True)
    country = CountryField(null=True)
    teamImg = models.ImageField(upload_to='team/teampictures/', blank=True)
    slug = models.SlugField(blank=True, null=True)
    members = models.ManyToManyField(Attendent, related_name="teammembers")

    # Models Storage related Methods
    def get_absolute_url(self):
        return reverse('portal:team_profile', args = [self.user.username])

    def __str__(self):
        return self.university

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Team, self).__init__(*args, **kwargs)
        self.slug = slugify(self.university)
        self.role = 'team'

    # Specific TEAM related Methods
    def get_ratings(self, year=datetime.now().year):
        """
        Used for Retrieving the Scoring Details on the Teams during the competition.
        Application Review Information is stored on the coresponding Application.
        """
        # Catch all given Feedback
        if self.feedback_set.all():
            # Calculate the AVG Values
            return self.feedback_set.filter(expert=self.user.attendent, date__year=year).aggregate(Avg('feedbackQuality'), Avg('feedbackRelated'), Avg('feedbackComm'))
        else:
            return None


class Staff(Attendent):
    """
    Every person that is part of the Organizing and Convention Team and gets
    assigned to Shifts of Work during the Competition Days.
    """
    role = models.CharField(choices=settings.STAFF_ROLES)
    def __init__(self, *args, **kwargs):
        super(Staff, self).__init__(*args, **kwargs)
        # Stores the periods during the convention days the person is available for
        # taking shifts
        availabilities = {}

#  ----------------- PROFILE SECTION ----------------------------------------

# ---Basic Profile Models to store additional Information on the Applicants
class Profile(models.Model):
    """
    Abstract Class to hold general information on the specific Profiles used for Teams, Student, Staff and Expert Assessors.
    As they widely vary in their scope and later usage, this split is meant to make code reuse easier.
    """
    class Meta:
        abstract = True

    user = models.OneToOneField(User, blank=True, null=True)
    bio = models.TextField(max_length=2000)
    slogan = models.CharField(max_length=250, verbose_name="Your favorite quote up to 250 characters")
    country = CountryField(null=True)
    city = models.CharField(max_length=50, verbose_name='City of Residence')
    profileImg = models.ImageField(upload_to='profileImg/%Y/%m/%d', blank=True)

    # Contact Details
    phoneNumber = models.CharField(verbose_name="Your Phone Number", max_length=100, blank=True, null=True)

    # Social Media Accounts
    twitter = models.URLField(verbose_name="Twitter Account",
    blank=True, null=True)
    linkedin = models.URLField(verbose_name="LinkedIn Account",
    blank=True, null=True)
    facebook = models.URLField(verbose_name="Facebook Account",
    blank=True, null=True)
    blog = models.URLField(verbose_name="Website",
    blank=True, null=True)

    # Models Storage related Methods
    def __str__(self):
        return str(self.user)

class ExpertProfile(Profile):
    """
    """
    team = models.ForeignKey(Team, related_name="coachedTeam", null=True, blank=True)  
    affiliation = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    # Special Certifications and Memberships
    imi_certified = models.BooleanField(verbose_name="Are you IMI Certified?", default=False)
    viac_member = models.BooleanField(verbose_name="Are you Member of VIAC?", default=False)
    iba_member = models.BooleanField(verbose_name="Are you Member of IBA?", default=False)

    def __str__(self):
        return str(self.user)

class StudentProfile(Profile):
    """
    Stores all relevant information on the Student as either(Negotiator, Mediator) in the
    competition. Is used for professional representation, sharing of information.
    It does NOT store relevant Scoringinformation etc.(= stored on ATTENDENT )
    """ 
    student = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)
    
    # relevant practical Experience
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('portal:student_profile', args=[self.user.username])

class TeamProfile(models.Model):
    """ Stores all relevant Information about the Team as the object of a Application.
    Relevant information about the Applicants as part of the team are stored in the
    'Student Profile' and assTociated to the Team Instance."""
    team = models.OneToOneField(Team, null=True, blank=True)
    languages_spoken = models.CharField(max_length=100, blank=True)

    # Application Relevant Information
    presentation_text = models.TextField(max_length=4000, blank=True)
    application_letter = models.FileField(verbose_name="Upload your motivation letter",
    upload_to='applications/teams/motivationletter/', 
    blank=True, null=True)

    application_video = models.FileField(verbose_name="Upload Application Video",
    blank=True, null=True) 

    # Additional Profile Information
    def __str__(self):
        return self.team.university
        
@receiver(post_save, sender=Team)
def create_tem_profile(sender, instance, created, **kwargs):
    if created:
        TeamProfile.objects.create(team=instance)

@receiver(post_save, sender=Team)
def save_team_profile(sender, instance, **kwargs):
    instance.teamprofile.save()

class StaffProfile(models.Model):
    """ Stores all relevant Information on the Staff Member used during their work
    at the competition, and their display on the webpage for representation.
    """
    pass         

#----------------- Interaction models -------------------------

# ----- Feedback / Scoring Views --------
def score_list(request):
    score_list = ScoreSheet.objects.filter(pk=request.user.id)
    return render(request, 'profile/score_list.html', {
        'score_list': score_list,
    })

def score_detail(request, session_slug):
    session_scores = ScoreSheet.objects.filter(pk=request.user.id)
    return render(request, 'profile/score_detail.html', {
        'session': session_slug,
        'session_scores': session_scores,
    })



#---------------   State models  --------------------------------
# Competencies
class Language(models.Model):
    """
    A professionaly relevant language competence in both written and spoken
    use.
    """
    LEVEL = (
        (1, 'basic communcation skills'),
        (2, 'good command'),
        (3, 'very good command'),
        (4, 'excellent command'),
        (5, 'near native'),
        (6, 'native speaker')
    )
    profile = models.ForeignKey(Profile, blank=True)
    name = models.CharField(max_length=50, verbose_name="Language")
    prof_written = models.IntegerField(choices=LEVEL,verbose_name="Written command")
    prof_spoken = models.IntegerField(choices=LEVEL, verbose_name="Verbal command")

    def __str__(self):
        return self.name

# Student Courses/Exmpeirnce
class Course(models.Model):
    """A relevant Course taken by a Student to be displayed in their profile"""
    profile = models.ForeignKey(Profile)
    subject = models.CharField(max_length=25, choices=PRACTICE_FIELDS)
    title = models.CharField(max_length=100)
    year = models.CharField(verbose_name="Year you have taken the course", max_length=20)
    instructor = models.CharField(max_length=70, blank=True, null=True)
    institution_abbr = models.CharField(max_length=10, blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(null=True)
    duration = models.IntegerField()
    measure = models.CharField(max_length=10)
    learnings = models.TextField(max_length=500, blank=True, null=True)
    def __str__(self):
        return "{}, {}".format(self.title, self.institution)

class Program(models.Model):
    """A relevant Course Offering by an Expert to be promoted on their profile"""
    expert = models.ForeignKey(ExpertProfile)
    subject = models.CharField(max_length=25, choices=PRACTICE_FIELDS)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    startDate = models.DateField(verbose_name='When does your Program start', blank=True, null=True)
    endDate = models.DateField(verbose_name="When does your Program end", blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(null=True)
    duration = models.IntegerField()
    webpage = models.URLField()

    def __str__(self):
        return self.title

class Internship(models.Model):
    profile = models.ForeignKey(Profile)
    position = models.CharField(max_length=150)
    field_of_practice = models.CharField(max_length=100, choices=PRACTICE_FIELDS)
    employer = models.CharField(max_length=100, verbose_name="Name of Firm or Instituation")
    country = CountryField(null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=4)
    duration = models.CharField(max_length=10, verbose_name="Duration")
    languages_used = models.CharField(max_length=250)
    descr = models.TextField(max_length=2500)

    def __str__(self):
        return self.position

class Competition(models.Model):
    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=100)
    country = CountryField(null=True)
    city = models.CharField(max_length=35)
    duration = models.CharField(max_length=50)
    measure = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    language = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Award(models.Model):
    profile = models.ForeignKey(Profile)
    competition = models.ForeignKey(Competition, null=True, blank=True)
    title = models.CharField(max_length=70, verbose_name='Award won')

    def __str__(self):
        return self.title
# Expert Professional Background Experience
class Certification(models.Model):
    profile = models.ForeignKey(ExpertProfile)
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=150)
    issueDate = models.DateField()
    def __str__(self):
        return self.institution

class Experience(models.Model):
    duration = models.IntegerField(verbose_name="Years of Experience in this role")
    cases = models.IntegerField(verbose_name="Number of engagements worked")
    description = models.TextField(verbose_name="Brief outline of the relevant professional background")
    priorClients = models.TextField(verbose_name="What key clients did you work with in this role?")
    placesWorked = models.TextField(verbose_name="Where did you work from/at?")

class MediationExperience(Experience):
    """Professional Experience in a given Field of Practice. Roles filled
    is used for judging the application. Additional Details can be provided."""
    ROLES = (
        (1, 'Practicing Mediator'),
        (2, 'Mediation Trainer'),
        (3, 'Judged Mediation Competitions'),
        (4, 'NO prior Experience')
    )
    profile = models.ForeignKey(ExpertProfile)
    profession = models.IntegerField(choices=ROLES)
    def __str__(self):
        # The 'get_..._display() returns the corresponding label
        return self.get_profession_display()

class NegotiationExperience(Experience):
    """Professional Experience in a given Field of Practice. Roles filled
    is used for judging the application. Additional Details can be provided."""
    ROLES = (
        (1, 'Practicing Negotiator'),
        (2, 'Negotiaton Trainer'),
        (3, 'Judged Negotiaton Competitions'),
        (4, 'NO prior Experience')
    )
    profile = models.ForeignKey(ExpertProfile)
    profession = models.IntegerField(choices=ROLES)
    def __str__(self):
        # The 'get_..._display() returns the corresponding label
        return self.get_profession_display()
