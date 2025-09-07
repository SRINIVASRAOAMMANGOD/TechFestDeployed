from django.urls import path
from django.views.generic import TemplateView
from . import views
from festapp.views import health_check
urlpatterns = [
    path('health', health_check, name='health_check'),

    # Home Page
    path('', TemplateView.as_view(template_name='festapp/index.html'), name='index'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Department
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_add'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_edit'),
    path('departments/<int:pk>/delete/', 
         lambda req, pk: views.safe_delete(req, "festapp", "Department", pk, "department_list", "department"),
         name="department_delete"),
# Export
path('export/', views.export_data, name='export_data'),

    # Student
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_add'),
    path('students/<int:pk>/edit/', views.student_update, name='student_edit'),
    path('students/<int:pk>/delete/', 
         lambda req, pk: views.safe_delete(req, "festapp", "Student", pk, "student_list", "student"),
         name="student_delete"),
# Registration
path('registrations/<int:pk>/edit/', views.registration_update, name='registration_edit'),

    # Venue
    path('venues/', views.venue_list, name='venue_list'),
    path('venues/add/', views.venue_create, name='venue_add'),
    path('venues/<int:pk>/edit/', views.venue_update, name='venue_edit'),
    path('venues/<int:pk>/delete/', 
         lambda req, pk: views.safe_delete(req, "festapp", "Venue", pk, "venue_list", "venue"),
         name="venue_delete"),

    # Event
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_create, name='event_add'),
    path('events/<int:pk>/edit/', views.event_update, name='event_edit'),
    path('events/<int:pk>/delete/', 
         lambda req, pk: views.safe_delete(req, "festapp", "Event", pk, "event_list", "event"),
         name="event_delete"),

   # Registration
path('registrations/', views.registration_list, name='registration_list'),
path('registrations/create/', views.registration_create, name='registration_create'),
path('registrations/<int:pk>/edit/', views.registration_update, name='registration_edit'),  # <-- added
path('registrations/<int:pk>/delete/', 
     lambda req, pk: views.safe_delete(req, "festapp", "Registration", pk, "registration_list", "registration"),
     name="registration_delete"),

# Winner
path('winners/', views.winner_list, name='winner_list'),
path('winners/create/', views.winner_create, name='winner_create'),
path('winners/<int:pk>/edit/', views.winner_update, name='winner_edit'),  # <-- added
path('winners/<int:pk>/delete/', 
     lambda req, pk: views.safe_delete(req, "festapp", "Winner", pk, "winner_list", "winner"),
     name="winner_delete"),


   
    # Organizer
    path('organizers/', views.organizer_list, name='organizer_list'),
    path('organizers/create/', views.organizer_create, name='organizer_create'),
    path('organizers/<int:pk>/edit/', views.organizer_update, name='organizer_edit'),
    path('organizers/<int:pk>/delete/', 
         lambda req, pk: views.safe_delete(req, "festapp", "Organizer", pk, "organizer_list", "organizer"),
         name="organizer_delete"),
]
