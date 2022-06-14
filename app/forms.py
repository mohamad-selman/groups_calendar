from django.forms import ModelForm, DateInput
from app.models import Event
from django.core.exceptions import ValidationError
from django import forms

# The event form
class EventForm(ModelForm):
  class Meta:
    model = Event

    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'owner' : forms.HiddenInput(),
    }

    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)

    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

    print(self.initial)

  # Validate that no two events overlaps
  def clean(self):
    super().clean()

    # The pending event
    participants = self.cleaned_data['participants']
    start1 = self.cleaned_data['start_time']
    end1 = self.cleaned_data['end_time']

    for p in participants:
      events = Event.objects.filter(participants = p).exclude(id = self.instance.id).values('start_time', 'end_time')

      # Existed events
      for e in events:
        start2 = e['start_time']
        end2 = e['end_time']

        if max(start1, start2) < min(end1, end2):
          raise ValidationError(f'Overlapping event for {p}')
