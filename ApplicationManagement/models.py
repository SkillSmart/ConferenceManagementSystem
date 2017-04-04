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

    def return_ratings(self):
        if applicant.role=='team':
            # Return team values
            pass

        else:
            # Return individual values
            pass


    def aggregate_ratings(self):
        # Check if Team or Student
        if self.applicant.role == "team":
            # all the function on all teammember applications
            # for member in self.applicant.team.members.all():
            #     member.get_current_application().aggregate_ratings()
            # Get the list of current member applications
            self.q1_score = self.applicant.team.members.all().aggregate(Avg('application__q1_score'))
            self.q2_score = self.applicant.team.members.all().aggregate(Avg('application__q2_score'))
            self.q3_score = self.applicant.team.members.all().aggregate(Avg('application__q3_score'))
            self.q4_score = self.applicant.team.members.all().aggregate(Avg('application__q4_score'))

            # Working Query for the Complete Average over all Application Ratings in Total
            results = Application.objects.all().annotate(q1_avg=Avg('review__question_1'), q2_avg=Avg('review__question_2'), q3_avg=Avg('review__question_3'), q4_avg=Avg('review__question_4')).aggregate(q1_score=Avg('q1_avg'), q2_score=Avg('q2_avg'), q3_score=Avg('q3_avg'), q4_score=Avg('q4_avg'))
            

            for member in self.applicant.team.members.all():
                scores 
            
            # # Aggregate the qx_score values on all applications; Store on self
            # self.q1_score = 
            # self.q2_score = members.aggregate(Avg('q2_score'))
            # self.q3_score = members.aggregate(Avg('q3_score'))
            # self.q4_score = members.aggregate(Avg('q4_score'))
        elif self.applicant.role =="mediator" or self.applicant.role=="negotiator" or self.applicant.role=="coach":
            # Treat this as student
            self.q1_score = self.review_set.aggregate(Avg('question_1'))
            self.q2_score = self.review_set.aggregate(Avg('question_2'))
            self.q3_score = self.review_set.aggregate(Avg('question_3'))
            self.q4_score = self.review_set.aggregate(Avg('question_4'))
        
        else: 
            return 'Did not recognize either student or team application'
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