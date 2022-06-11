from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:event_id>', views.event, name='event_edit'),
]