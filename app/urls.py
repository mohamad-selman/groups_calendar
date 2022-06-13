from django.urls import path
from app import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logout_u, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('calendar/', login_required(views.CalendarView.as_view(), login_url='home'), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:event_id>', views.event, name='event_edit'),
    path('event/delete/<int:event_id>', views.delete_event, name='event_delete'),
]
