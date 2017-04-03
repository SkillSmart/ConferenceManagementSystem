from django.db import models
from random import randint
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
    continent_rank = None
    overall_rank = None

    # The Application review scores for this application
    q1_score = models.FloatField(blank=True, null=True)
    q2_score = models.FloatField(blank=True, null=True)
    q3_score = models.FloatField(blank=True, null=True)
    q4_score = models.FloatField(blank=True, null=True)

    def aggregate_ratings(self):
        # Check if Team or Student
        if self.applicant.role =="mediator" or self.applicant.role=="negotiator" or self.applicant.role=="coach":
            # Treat this as student
            self.q1_score = self.review_set.aggregate(Avg('question_1'))
            self.q2_score = self.review_set.aggregate(Avg('question_2'))
            self.q3_score = self.review_set.aggregate(Avg('question_3'))
            self.q4_score = self.review_set.aggregate(Avg('question_4'))

        elif self.applicant.role == "team":
            # Collect the list of all member applications
            members = self.applicant.team.members.all()
            # Get the list of current member applications
            q1 
            for member in members:
                apl = member.get_current_application()
                apl.aggregate_ratings()
                ratings['q1_score'].append(apl.q1_score)
                ratings['q2_score'].append(apl.q2_score)
                ratings['q3_score'].append(apl.q2_score)
                ratings['q4_score'].append(apl.q2_score)
            
            return ratings
            # # Aggregate the qx_score values on all applications; Store on self
            # self.q1_score = 
            # self.q2_score = members.aggregate(Avg('q2_score'))
            # self.q3_score = members.aggregate(Avg('q3_score'))
            # self.q4_score = members.aggregate(Avg('q4_score'))
        else:
            # Treat as Expert
            pass
        return
        # If Student then calculate ratings over all reviews and store on the Attendent
        # If Team then call the calculation method on all members and then calculate the Sum

        # return None

    def __str__(self):
        return "{}-{}".format(self.applicant.user.username, self.competition_year)

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        # Summary Scores calculated on the Application instance
        self.score = randint(1,5)
        self.continent_rank = randint(1,25)
        self.overall_rank = randint(1,25)

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
        self.application.status = 1
        super().save(*args, **kwargs)
        

class Feedback(models.Model):
    """
    Feedback given by a participating student to a judge at a session
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    expert = models.ForeignKey(Attendent, on_delete=models.CASCADE)

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