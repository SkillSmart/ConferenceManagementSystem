# Demonstrating the use of model managers in django

from SessionManagement.models import Session
from django.db.models.manager import Manager
from django.db.utils import get_or_create
import datetime
from SessionManagement.models import Venue

class SessionManager(Manager):
    def by_day(self, day):
        return self.get_queryset().filter(
            start_time__gte=datetime.date(day,0,0),
            start_time__lte=datetime.date(day, 23, 59)
        )
    def today(self):
        return self.get_queryset().filter(
            start_time__gte=datetime.now().day()
        )

# This examplies the use of a model manager to manage the automatic creation of a complex model 
class NewSessionManager(SessionManager):
    def new_session(self, session_name, venue, room, start_time, end_time:
        session = Session.objects.get_or_create(name=session_name)[0]
        venue = Venue.objects.get_or_create(
            name=venue,
            room=room,
            start_time=start_time,
            end_time=end_time
            )[0]
        
        song = self.model(titel=song_title,
            artist=artist,
            album=album)
        song.save()

        return song

        