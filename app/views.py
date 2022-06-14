from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm

# For landing page
def index(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to the calendar
        return HttpResponseRedirect(reverse('calendar'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate users who are logging in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the calendar after authentication
            return HttpResponseRedirect(reverse('calendar'))

    # Render a login page to non-authenticated users
    return render(request, './login.html')

# Logs out a user
def logout_u(request):
    logout(request)

    # Redirect to the initial landing page
    return redirect('home')

# Takes data from registration form and creates new account for user
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if username is already used
        if User.objects.filter(username=username).exists():
            return render(request, './signup.html', {'used': True})
    
        User.objects.create_user(password=password, username=username)
        # Redirect to homepage where user can login
        return redirect('home')

    # Render the registration page (form)
    return render(request, './signup.html')

# Calendar 
class CalendarView(ListView):
    model = Event # Data
    template_name = 'calendar.html' # HTML Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, self.request.user.id)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

# Returns current date and time
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

# Change the calendar to the previous month
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

# Change the calendar to the next month
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# To modify and create new events
@login_required(login_url='home')
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    # A user can modify an event if he/she is the owner or a group member
    # Can delete an event if he/she is the owner
    can_submit = True
    can_delete = False

    if event_id:
        is_owner = Event.objects.filter(id=event_id, owner_id=request.user.id) # Check if the owner
        is_group_member = Event.objects.filter(id=event_id, participants=request.user.id) # Check if member of the group

        can_submit = (is_owner | is_group_member).exists()
        can_delete = is_owner.exists()

    form = EventForm(request.POST or None, instance=instance, initial={'owner': request.user.id})

    if request.POST and form.is_valid():
        form.save() # Create new event
        return HttpResponseRedirect(reverse('calendar')) # Redirect to the calendar

    context = {
        'form': form,
        'can_submit': can_submit,
        'can_delete' : can_delete,
        'event_id': event_id
    }
    return render(request, 'event.html', context)

# To delete events
@login_required(login_url='home')
def delete_event(request, event_id=None):
    Event.objects.filter(id=event_id).delete()
    return HttpResponseRedirect(reverse('calendar')) # Redirect to the calendar
