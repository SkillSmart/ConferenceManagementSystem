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

    STATUS = (
        (0, 'Declined'),
        (1, 'Unreviewed'),
        (2, 'Reviewed'),
        (3, 'Selected'),
        (4, 'Accepted')
    )

    applicant = models.ForeignKey(Attendent)
    competition_year = models.CharField(max_length=4)
    applicationDate = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    term_accepted = models.BooleanField(default=False, verbose_name="Accept Legal Terms")

    # Application Result variables
    continent_rank = models.IntegerField()
    overall_rank = models.IntegerField()

    # The Application review scores for Individual Applications
    q1_score = models.FloatField(blank=True, null=True)
    q2_score = models.FloatField(blank=True, null=True)
    q3_score = models.FloatField(blank=True, null=True)
    q4_score = models.FloatField(blank=True, null=True)
    
    # The Total Application Score (Total Average over all Dimension Scores)
    application_score = models.FloatField(blank=True, null=True)


    def get_ratings(self):
        # Update Ratings (TODO: Add check to see if there are changes, if not return cached)
        #  (........)
        if self.applicant.role =="team":
            scores = self.aggregate_ratings() 

        # If new reviews where added, update the Scoring      
        self.aggregate_ratings()
        # Return the Value as a dict
        return {self.applicant: [self.q1_score, self.q2_score, 
                                self.q3_score, self.q4_score]}


    def update_ratings(self):
        """
        Uses a 'switch' on the instance application.applicant.role to call appropriate aggregation
        methods to calculate the current application score, and store them on the instance itself.
        Does not return values directly to the calling instance.
        """
        STUDENTROLES = ['mediator', 'negotiator', 'coach']
        EXPERTROLES = ['expert']
        # Check if Team or Student
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
            self.application_score = total_team_score
            self.q1_score = team_avg_scores[0]
            self.q2_score = team_avg_scores[1]
            self.q3_score = team_avg_scores[2]
            self.q4_score = team_avg_scores[3]
            self.save()

        elif self.applicant.role in EXPERTROLES:
            # Treat this as an expert (Aggregate Student Feedback received on their performance)
            pass
        
        elif self.applicant.role in STUDENTROLES:
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

    def get_rank(self, total=True):
        """
        Either gets the Ranking for Individuals (Student, Expert) or for Teams based on their
        specific evaluation metrics (StudentFeedback, Assessor Scores, Averaged Team Member Scores).
        The total argument sets the comparison to either 'continental' or 'total overall' ranking.
        """
        pass

    def __str__(self):
        return "{}-{}".format(self.applicant.user.username, self.competition_year)

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        
        # Team Application specific values - Saved on the Instance
        member_avg_scores = None
        team_avg_scores = None
        

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