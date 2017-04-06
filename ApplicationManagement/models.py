from django.db import models
from django.conf import settings
# Helper Libraries
from random import randint
from pandas import DataFrame
# Import Entity models
from django.contrib.auth.models import User
from UserManagement.models import Student, Expert, Team, Staff
from SessionManagement.models import Session
# Import for Summary Statistics on the Models
from django.db.models import (Sum, Max, Min, Avg, StdDev)

# Create your models here.
class Application(models.Model):
    """ Application issued by an Attendant for a given year.
    Application holds information on pre-acceptance processess
    Continous information about demeanor of Attendant is stored in the
    Attendent instance."""

    class Meta:
        unique_together = ('applicant', 'competition_year')
        abstract = True

    # Application Status set for tracking the decission process during application review
    REVIEW_STATUS = (
        (0, 'Unreviewed'),
        (1, 'In Review'),
        (2, 'Reviewed'),
        (3, 'Selected')
    )
    SELECTION_STATUS = (
        (1, 'None'),
        (2, 'Declined'),
        (3, 'Accepted')
    )

    application_type = models.CharField(max_length=20, null=True)
    competition_year = models.CharField(max_length=4)
    applicationDate = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    # Variables controlling when an application can be finally accepted
    term_accepted = models.BooleanField(default=False, verbose_name="Accept Legal Terms")    
    review_status = models.IntegerField(choices=REVIEW_STATUS, default=1)
    review_completed = models.BooleanField(default=False, verbose_name="Application review complete")
    selection_status = models.IntegerField(choices=SELECTION_STATUS, default=1)
    # Application Result variables
    continent_rank = models.IntegerField(blank=True, null=True)
    overall_rank = models.IntegerField(blank=True, null=True)

    # The Application review scores for Individual Applications
    q1_score = models.FloatField(blank=True, null=True)
    q2_score = models.FloatField(blank=True, null=True)
    q3_score = models.FloatField(blank=True, null=True)
    q4_score = models.FloatField(blank=True, null=True)
    
    # The Total Application Score (Total Average over all Dimension Scores)
    application_score = models.FloatField(blank=True, null=True)



    def update_review_status(self):
        """
        Based on a 'switch' on the instance application.application_type it decides how to check if
        the application instance is completed for final submission/approval.
        It sets the variable self.status accordingly.
        When ready for submission, self.review_completed is set to TRUE.
        """
        if self.application_type == 'student':
            """
            Student Applications are to be reviewed by all 'Raters' to be considered finished.
            Each Rater can only submit one Review per Application.
            Once the application has received their first review, they are inbetween 'unreviewed' and 
            'reviewed'
            """
            application_reviews = self.review_set.all()
            if application_reviews and (application_reviews.count() == Expert.objects.count()):
                self.review_status = '2'
                self.review_completed = True
                self.save()
            else:
                self.review_status = '1'
                self.review_completed = False
                self.save()
            return None
        elif self.application_type == 'expert':
            return
        elif self.application_type == 'team':
            # Team application is completly reviewed when all its associated student
            # applications have review_completed

            # Check for completed Review of all member Applications
            def teamreview_done(self):
                for application in self.applicant.members.all():
                    if application.review_completed == False: 
                        return False
                return True
            # Check if team has been successfully reviewed, and if so store the information
            # on the team application
            if teamreview_done():
                self.review_completed = True
                self.review_status = 2
            
        elif self.application_type == 'staff':
            return None

    def force_reviewed(self, all=False):
        """
        Convencience Function to let ADMIN force the finalization of the Review Process
        on an application. 
        As not all raters will ever rate every application, this can be overwritten
        for either a single application or for all of them at once. (all=True)
        """
        if all:
            for application in Application.objects.filter(application_type=self.application_type):
                if review_status < 2:
                    review_status = 2
        else:
            if self.review_status < 2:
                self.review_status = 2
        self.save()

    def update_ratings(self):
        """
        Uses a 'switch' on the instance application.application_type to call appropriate aggregation
        methods to calculate the current application score, and store them on the instance itself.
        Does not return values directly to the calling instance.
        """

        # Check if Team or Student or Expert
        if self.application_type == "team":
            # Treat as Team with members to be aggregated and a total to then be calculated
            member_avg_scores = {}
            members = self.applicant.members.all()
            for member in members:
                member_avg_scores[member] = member.get_current_application().review_set.all().aggregate(d1_avg=Avg('question_1'), d2_avg=Avg('question_2'), d3_avg=Avg('question_3'), d4_avg=Avg('question_4'))    
            
            # Calculate Team Average Scores for all Assessor Dimensions
            team_avg_scores = DataFrame.from_dict(member_avg_scores, orient='index').mean(axis=0)
            total_team_score = team_avg_scores.mean()
            
            # Update Values on the Instance
            self.team_avg_scores = team_avg_scores
            self.member_avg_scores = member_avg_scores
            self.memberreview_score = total_team_score
            self.application_score = (self.videoreview_score + self.memberreview_score)/2
            self.q1_score = team_avg_scores[0]
            self.q2_score = team_avg_scores[1]
            self.q3_score = team_avg_scores[2]
            self.q4_score = team_avg_scores[3]
            self.save()
            
        elif self.application_type == 'expert':
            """
            Experts apply either for the first time, or they have already taken part in an earlier
            Convention. If so, they received Feedback and their performance is important.
            If NOT: Then this calculation can be skipped.
            """
            # Did he/she already judge here before? (They received Feedback)
            if self.applicant.feedback_set:
                # Check for how many years already
                feedback_years = []
                for feedback in self.applicant.feedback_set.all():
                    if feedback.date.year not in feedback_years:
                        feedback_years.append(feedback.date.year)
                # Calculate the ratings for all available years individually
                ratings = {}
                for year in feedback_years:
                    ratings[year] = self.applicant.get_ratings(year=year)
            # Treat this as an expert (Aggregate Student Feedback received on their performance)
            
            
            # Get the distinct years of feedback on this person
            feedback_years = []
            for feedback in expert.applicant.feedback_set.all():
                if feedback.date.year not in feedback_years:
                    feedback_years.append(feedback.date.year)
            
            # Call the Attendent instance to retrieve the ratings for the given years
            ratings = {}
            for year in feedback_years:
                ratings[year] =  self.applicant.get_ratings(year=year)
        

        elif self.application_type == 'student':
            # Treat this as student
            avg_scores = self.review_set.all().aggregate(d1_avg = Avg('question_1'),
                                                        d2_avg = Avg('question_2'),
                                                        d3_avg = Avg('question_3'),
                                                        d4_avg = Avg('question_4'))
            # Assign values to instance variables
            self.q1_score = avg_scores['d1_avg']
            self.q2_score = avg_scores['d2_avg']
            self.q3_score = avg_scores['d3_avg']
            self.q4_score = avg_scores['d4_avg']
            # Calculate overall total Avg
            # self.application_score = DataFrame.from_dict(avg_scores).mean(axis=0)
            self.save()
        else: 
            return 'Did not recognize either student or team application'


    def update_rank(self, total=True):
        """
        Either gets the Ranking for Individuals (Student, Expert) or for Teams based on their
        specific evaluation metrics (StudentFeedback, Assessor Scores, Averaged Team Member Scores).
        The total argument sets the comparison to either 'continental' or 'total overall' ranking.
        """
        # When ranking on the Global Rankinglist
        if total:
            # Switch on the type of application
            def update_list(self, queryset_ranked):
                """Used to update the whole list of resulting objects"""
                for index, application in enumerate(queryset_ranked):
                    application.overall_rank = index + 1
                    application.save()

            if self.application_type == "team":
                # Create an ordered list of the teams on (application_score)
                self.update_list(TeamApplication.objects.order_by('-application_score'))
            
            elif self.application_type == 'expert':
                # Create an ordered list of all experts based on review scores
                self.update_list(ExpertApplication.objects.order_by('-application_score'))

            
            elif self.application_type == 'student':
                pass
            elif self.application_type == 'staff':
                pass

    def __str__(self):
        return "{}-{}".format(self.applicant.user.username, self.competition_year)

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        # Team Application specific values - Saved on the Instance

class ExpertApplication(Application):
    """ Application for a Expert Assessment Role
    """
    applicant = models.ForeignKey(Expert, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.EXPERT_ROLES)

    def __init__(self, *args, **kwargs):
        self.application_type = 'expert'
        member_avg_scores = None
        team_avg_scores = None

class StudentApplication(Application):
    """
    A Student application as part of a team application with the CDRC Competition.
    Each Student is only allowed to partace once in the Competition in this role.
    To ensure this, there is a one to one relation between the student Model and
    the user that is registered with the System.
    """
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.STUDENT_ROLES)

    def __init__(self, *args, **kwargs):
        super(StudentApplication, self).__init__(*args, **kwargs)
        self.application_type = 'student'

class TeamApplication(Application):
    """
    A Team application is started without beeing registered to a particular set 
    of members. Within the Team Application Process, the Team members are entered
    into the system and become associated with the particular instance of this application.
    Each Student can only be registered with a team, and one team only. 
    Each User can only be registerd with one application
    """
    class Meta:
        unique_together = ('applicant', 'member_applications')
    
    applicant = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.TEAM_ROLES)
    # Associated Team Member Applicationset (These are the ones beeing rated)
    member_applications = models.ManyToManyField(StudentApplication)
    # Specific Variables only relevant to a Team
    videoreview_score = models.FloatField(blank=True, null=True)
    memberreview_score = models.FloatField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(TeamApplication, self).__init__(*args, **kwargs)
        self.application_type = 'team'
            # Team relevant Scores
   

class StaffApplication(Application):
    """
    A Staff application is send to register a person with the CDRC Team. It represents the 
    review and comments made on the person, and is stored in the system for later review.
    Associated information from the Application is used to prepopulate the Staff Profile, 
    once the Application has been accepted.
    """
    applicant = models.ForeignKey(Staff, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.STAFF_ROLES)
    
    # Specific Application Values for Staff
    ## Contact Information
    phone = models.CharField(max_length=20, null=True)
        # To be filled

    def __init__(self, *args, **kwargs):
        super(StaffApplication, self).__init__(*args, **kwargs)
        self.applcation_type = 'staff'
        # Specific Staff Variables
        availabilities = {} # Stores the timeslots available for Shifts (Date, Time)


# ------- Application related Classes [Feedback and Reviews Models] ------------
class Review(models.Model):
    """Base Class for both Expert and Student Reviews. Externally done by
    Commitee Members and associated to a specific Application, 
    not the Userclass"""

    class Meta:
        # Each Reviewer can review a given Application only once
        unique_together = ('reviewer', 'application')
    
    application = models.ForeignKey(Application)
    reviewer = models.ForeignKey(User)

    # Questions to be answered
    SELECTION = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    # Applicatino Reviews Dimensions
    question_1 = models.IntegerField(choices=SELECTION, verbose_name="Question 1")
    question_2 = models.IntegerField(choices=SELECTION, verbose_name="Question 2")
    question_3 = models.IntegerField(choices=SELECTION, verbose_name="Question 3")
    question_4 = models.IntegerField(choices=SELECTION, verbose_name="Question 4")

    # Additional comments
    comment = models.TextField(max_length=250, blank=True)
    
    def __str__(self):
        return "{}'s Application reviewed by {}".format(self.application, self.reviewer)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Engage the application to update its ratings, now that there is 
        # a new review
        self.application.update_ratings()
        # Update the review status
        self.application.update_review_status()
        

class Feedback(models.Model):
    """
    Feedback given by a participating student to an Expert Assessor at a specific session
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    date = models.DateTimeField()

    # Feedback Categories
    feedbackQuality = models.IntegerField(verbose_name="How helpfull was his/her Feedback?",
                                            blank=True, null=True)
    feedbackRelated = models.IntegerField(verbose_name="How well did the Feedback relate to the Assessment Criteria?",
                                             blank=True, null=True)
    feedbackComm = models.IntegerField(verbose_name="How well was the Feedback Communicated?",
                                             blank=True, null=True)

    # Free Text Feedback
    text = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "{} - {}, {}".format(self.session, self.expert.user.last_name, self.expert.user.first_name)

    def save(self, *args, **kwargs):
        self.date = self.session.startTime
        super(Feedback, self).save(*args, **kwargs)