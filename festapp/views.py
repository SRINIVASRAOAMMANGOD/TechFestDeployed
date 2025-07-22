from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Department, Student, Venue, Event, Registration, Winner, Organizer
from .forms import DepartmentForm, StudentForm, VenueForm, EventForm, RegistrationForm, WinnerForm, OrganizerForm

# Home Page
class HomeView(TemplateView):
    template_name = 'festapp/index.html'


# ---------- Department Views ----------
class DepartmentListView(ListView):
    model = Department
    template_name = 'festapp/department_list.html'

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'festapp/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'festapp/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('department_list')


# ---------- Student Views ----------
class StudentListView(ListView):
    model = Student
    template_name = 'festapp/student_list.html'

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'festapp/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'festapp/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('student_list')


# ---------- Venue Views ----------
class VenueListView(ListView):
    model = Venue
    template_name = 'festapp/venue_list.html'

class VenueCreateView(CreateView):
    model = Venue
    form_class = VenueForm
    template_name = 'festapp/venue_form.html'
    success_url = reverse_lazy('venue_list')

class VenueUpdateView(UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = 'festapp/venue_form.html'
    success_url = reverse_lazy('venue_list')

class VenueDeleteView(DeleteView):
    model = Venue
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('venue_list')


# ---------- Event Views ----------
class EventListView(ListView):
    model = Event
    template_name = 'festapp/event_list.html'

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'festapp/event_form.html'
    success_url = reverse_lazy('event_list')

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'festapp/event_form.html'
    success_url = reverse_lazy('event_list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('event_list')


# ---------- Registration Views ----------
class RegistrationListView(ListView):
    model = Registration
    template_name = 'festapp/registration_list.html'

class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'festapp/registration_form.html'
    success_url = reverse_lazy('registration_list')

class RegistrationUpdateView(UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'festapp/registration_form.html'
    success_url = reverse_lazy('registration_list')

class RegistrationDeleteView(DeleteView):
    model = Registration
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('registration_list')


# ---------- Winner Views ----------
class WinnerListView(ListView):
    model = Winner
    template_name = 'festapp/winner_list.html'

class WinnerCreateView(CreateView):
    model = Winner
    form_class = WinnerForm
    template_name = 'festapp/winner_form.html'
    success_url = reverse_lazy('winner_list')

class WinnerUpdateView(UpdateView):
    model = Winner
    form_class = WinnerForm
    template_name = 'festapp/winner_form.html'
    success_url = reverse_lazy('winner_list')

class WinnerDeleteView(DeleteView):
    model = Winner
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('winner_list')


# ---------- Organizer Views ----------
class OrganizerListView(ListView):
    model = Organizer
    template_name = 'festapp/organizer_list.html'

class OrganizerCreateView(CreateView):
    model = Organizer
    form_class = OrganizerForm
    template_name = 'festapp/organizer_form.html'
    success_url = reverse_lazy('organizer_list')

class OrganizerUpdateView(UpdateView):
    model = Organizer
    form_class = OrganizerForm
    template_name = 'festapp/organizer_form.html'
    success_url = reverse_lazy('organizer_list')

class OrganizerDeleteView(DeleteView):
    model = Organizer
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('organizer_list')
