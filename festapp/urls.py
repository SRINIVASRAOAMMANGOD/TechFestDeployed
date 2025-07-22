from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='festapp/index.html'), name='index'),

    # Department
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    #path('departments/', views.department_list, name='department_list'),

    path('departments/add/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Student
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # Venue
    path('venues/', views.VenueListView.as_view(), name='venue_list'),
    path('venues/add/', views.VenueCreateView.as_view(), name='venue_add'),
    path('venues/<int:pk>/edit/', views.VenueUpdateView.as_view(), name='venue_edit'),
    path('venues/<int:pk>/delete/', views.VenueDeleteView.as_view(), name='venue_delete'),

    # Event
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/add/', views.EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # Registration
    path('registrations/', views.RegistrationListView.as_view(), name='registration_list'),
    path('registrations/add/', views.RegistrationCreateView.as_view(), name='registration_add'),
    path('registrations/<int:pk>/edit/', views.RegistrationUpdateView.as_view(), name='registration_edit'),
    path('registrations/<int:pk>/delete/', views.RegistrationDeleteView.as_view(), name='registration_delete'),

    # Winner
    path('winners/', views.WinnerListView.as_view(), name='winner_list'),
    path('winners/add/', views.WinnerCreateView.as_view(), name='winner_add'),
    path('winners/<int:pk>/edit/', views.WinnerUpdateView.as_view(), name='winner_edit'),
    path('winners/<int:pk>/delete/', views.WinnerDeleteView.as_view(), name='winner_delete'),

    # Organizer
    path('organizers/', views.OrganizerListView.as_view(), name='organizer_list'),
    path('organizers/add/', views.OrganizerCreateView.as_view(), name='organizer_add'),
    path('organizers/<int:pk>/edit/', views.OrganizerUpdateView.as_view(), name='organizer_edit'),
    path('organizers/<int:pk>/delete/', views.OrganizerDeleteView.as_view(), name='organizer_delete'),
]
