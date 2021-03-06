from django.db import models
from random import randint
from pandas import DataFrame
# Import Entity models
from django.contrib.auth.models import User
from UserManagement.models import Attendent, Team
from SessionManagement.models import Session
# Import for Summary Statistics on the Models
from django.db.models import (Sum, Max, Min, Avg, StdDev)

# Create your models here.
class Application(models.Model):
    """ Application issued by an Attendant for a given year.
    Application holds information on pre-acceptance processess
    Continous information about demeanor of Attendant is stored in the
    Attendent instance."""
    # General Information on the possible Roles for a student, expert and team
    STUDENTROLES = ['mediator', 'negotiator', 'coach']
    EXPERTROLES = ['expert']

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

    applicant = models.ForeignKey(Attendent)
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
    # Team relevant Scores
    videoreview_score = models.FloatField(blank=True, null=True)
    memberreview_score = models.FloatField(blank=True, null=True)

    def get_review_status(self):
        """
        Based on a 'switch' on the instance application.applicant.role it decides how to check if
        the application instance is completed for final submission/approval.
        It sets the variable self.status accordingly.
        When ready for submission, self.review_completed is set to TRUE.
        """
        if self.application_type in self.STUDENTROLES:
            """
            Student Applications are to be reviewed by all 'Raters' to be considered finished.
            Each Rater can only submit one Review per Application.
            Once the application has received their first review, they are inbetween 'unreviewed' and 
            'reviewed'
            """
            application_reviews = self.review_set.all()
            if application_reviews and (application_reviews.count() == Attendent.objects.filter(role='expert'.count())):
                self.status = '2'
                self.review_completed = True
                self.save()
            else:
                self.status = '1'
                self.review_completed = False
                self.save()
            return none
        elif self.application_type in self.EXPERTROLES:
            return
        elif self.applicaton_type == 'team':
            return

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
        Uses a 'switch' on the instance application.applicant.role to call appropriate aggregation
        methods to calculate the current application score, and store them on the instance itself.
        Does not return values directly to the calling instance.
        """

        # Check if Team or Student or Expert
        if self.applicant.role == "team":
            # Treat as Team with members to be aggregated and a total to then be calculated
            member_avg_scores = {}
            members = self.applicant.team.members.all()
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
            
        elif self.applicant.role in self.EXPERTROLES:
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
        

        elif self.applicant.role in self.STUDENTROLES:
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
        # If Student then calculate ratings over all reviews and store on the Attendent
        # If Team then call the calculation method on all members and then calculate the Sum

        # return None

    def update_rank(self, total=True):
        """
        Either gets the Ranking for Individuals (Student, Expert) or for Teams based on their
        specific evaluation metrics (StudentFeedback, Assessor Scores, Averaged Team Member Scores).
        The total argument sets the comparison to either 'continental' or 'total overall' ranking.
        """
        if self.applicant.role == "team":
            # Create an ordered list of the teams on (application_score)
            teamapplications_ranked = Application.objects.filter(applicant__role='team').order_by('-application_score')
            # Update all teamapplications with the appropriate rank
            for index, teamapplication in enumerate(teamapplications_ranked):
                teamapplication.overall_rank = index + 1
                teamapplication.save()


    def __str__(self):
        return "{}-{}".format(self.applicant.user.username, self.competition_year)

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        # Team Application specific values - Saved on the Instance
        member_avg_scores = None
        team_avg_scores = None
        # Set initial values on the instnace variable
        self.application_type = self.applicant.role

    class Meta:
        unique_together = ('applicant', 'competition_year')

class Review(models.Model):
    """Base Class for both Expert and Student Reviews. Externally done by
    Commitee Members and associated to a specific Application, 
    not the Userclass"""

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

    question_1 = models.IntegerField(choices=SELECTION, verbose_name="Question 1")
    question_2 = models.IntegerField(choices=SELECTION, verbose_name="Question 2")
    question_3 = models.IntegerField(choices=SELECTION, verbose_name="Question 3")
    question_4 = models.IntegerField(choices=SELECTION, verbose_name="Question 4")

    # Additional comments
    comment = models.TextField(max_length=250, blank=True)

    class Meta:
        unique_together = ('reviewer', 'application')
    
    def __str__(self):
        return "{}'s Application reviewed by {}".format(self.application, self.reviewer)

    def save(self, *args, **kwargs):
        self.application.status = 0
        super().save(*args, **kwargs)
        

class Feedback(models.Model):
    """
    Feedback given by a participating student to a judge at a session
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    expert = models.ForeignKey(Attendent, on_delete=models.CASCADE)
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