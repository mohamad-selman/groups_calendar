from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import F, Q

'''
An Event has the following attributes:
    A unique id
    A title
    An optional description
    Start date and time
    End date and time
    An owner (user who created the event)
    A boolean called private (indicate whether an event is public or private)
    A list of users who are part of the event (only owner or a group)
'''
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default=None, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Event_owner")
    private = models.BooleanField(default=False, blank=True)
    participants = models.ManyToManyField(User)

    # Validate that ending time is after the starting time
    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('Start time is after end time')
        if self.start_time == self.end_time:
            raise ValidationError('Start and end time are at the same time')


    # Returns URL of the event
    @property
    def get_url(self):
        url = reverse('event_edit', kwargs={'event_id': self.id})
        return f'''
                    <a href="{url}">
                        {self.title}
                    </a>
        '''

    class Meta:
        db_table = 'Event'

        constraints = [
            models.CheckConstraint(
                check=Q(end_time__gt=F('start_time')),
                name="endtime_CHK"
            )
        ]

