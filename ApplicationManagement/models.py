from django.db import models
from random import randint
# Import Entity models
from django.contrib.auth.models import User
from UserManagement.models import Attendent, Team
from SessionManagement.models import Session

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

    # TODO: Turn this into actual scoring method (Instead of faking with __init__)
    def get_ratingscore(self):
        ratings = self.review_set.all()
        score = int(2.3)
        return int(2.3)

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
    session = models.ForeignKey(Session)
    expert = models.ForeignKey(Attendent)

    # Feedback Categories
    category_1 = models.IntegerField(verbose_name="How helpfull was his/her Feedback")
    category_2 = models.IntegerField(verbose_name="How personal did you feel the Feedback was")
    category_3 = models.IntegerField(verbose_name="How easy was it to put the Feedback into action")
    category_4 = models.IntegerField(verbose_name="How clear and elaborate was the Experts Feedback")

    # Free Text Feedback
    text = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "{} - {}, {}".format(self.session, self.expert.user.last_name, self.expert.user.first_name)