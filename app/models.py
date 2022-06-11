from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default=None, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

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

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Participation'
        unique_together = (('user', 'event'),)
