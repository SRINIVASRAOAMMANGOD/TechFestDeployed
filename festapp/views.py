from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Department, Student, Venue, Event, Registration, Winner, Organizer
from .forms import DepartmentForm, StudentForm, VenueForm, EventForm, RegistrationForm, WinnerForm, OrganizerForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
def user_logout(request):
    logout(request)
    return redirect('index') 
class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # or any page
        else:
            return render(request, 'festapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'festapp/login.html')
# Home Page
class HomeView(TemplateView):
    template_name = 'festapp/index.html'


# ---------- Department Views ----------
class DepartmentListView(ListView):
    model = Department
    template_name = 'festapp/department_list.html'

class DepartmentCreateView(AdminOnlyMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'festapp/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(AdminOnlyMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'festapp/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentDeleteView(AdminOnlyMixin, DeleteView):
    model = Department
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('department_list')


# ---------- Student Views ----------
class StudentListView(ListView):
    model = Student
    template_name = 'festapp/student_list.html'

class StudentCreateView(AdminOnlyMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'festapp/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(AdminOnlyMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'festapp/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(AdminOnlyMixin, DeleteView):
    model = Student
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('student_list')


# ---------- Venue Views ----------
class VenueListView(ListView):
    model = Venue
    template_name = 'festapp/venue_list.html'

class VenueCreateView(AdminOnlyMixin, CreateView):
    model = Venue
    form_class = VenueForm
    template_name = 'festapp/venue_form.html'
    success_url = reverse_lazy('venue_list')

class VenueUpdateView(AdminOnlyMixin, UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = 'festapp/venue_form.html'
    success_url = reverse_lazy('venue_list')

class VenueDeleteView(AdminOnlyMixin, DeleteView):
    model = Venue
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('venue_list')


# ---------- Event Views ----------
class EventListView(ListView):
    model = Event
    template_name = 'festapp/event_list.html'

class EventCreateView(AdminOnlyMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'festapp/event_form.html'
    success_url = reverse_lazy('event_list')

class EventUpdateView(AdminOnlyMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'festapp/event_form.html'
    success_url = reverse_lazy('event_list')

class EventDeleteView(AdminOnlyMixin, DeleteView):
    model = Event
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('event_list')


# ---------- Registration Views ----------
class RegistrationListView(ListView):
    model = Registration
    template_name = 'festapp/registration_list.html'

class RegistrationCreateView(AdminOnlyMixin, CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'festapp/registration_form.html'
    success_url = reverse_lazy('registration_list')

class RegistrationUpdateView(AdminOnlyMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'festapp/registration_form.html'
    success_url = reverse_lazy('registration_list')

class RegistrationDeleteView(AdminOnlyMixin, DeleteView):
    model = Registration
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('registration_list')


# ---------- Winner Views ----------
class WinnerListView(ListView):
    model = Winner
    template_name = 'festapp/winner_list.html'

class WinnerCreateView(AdminOnlyMixin, CreateView):
    model = Winner
    form_class = WinnerForm
    template_name = 'festapp/winner_form.html'
    success_url = reverse_lazy('winner_list')

class WinnerUpdateView(AdminOnlyMixin, UpdateView):
    model = Winner
    form_class = WinnerForm
    template_name = 'festapp/winner_form.html'
    success_url = reverse_lazy('winner_list')

class WinnerDeleteView(AdminOnlyMixin, DeleteView):
    model = Winner
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('winner_list')


# ---------- Organizer Views ----------
class OrganizerListView(ListView):
    model = Organizer
    template_name = 'festapp/organizer_list.html'

class OrganizerCreateView(AdminOnlyMixin, CreateView):
    model = Organizer
    form_class = OrganizerForm
    template_name = 'festapp/organizer_form.html'
    success_url = reverse_lazy('organizer_list')

class OrganizerUpdateView(AdminOnlyMixin, UpdateView):
    model = Organizer
    form_class = OrganizerForm
    template_name = 'festapp/organizer_form.html'
    success_url = reverse_lazy('organizer_list')

class OrganizerDeleteView(AdminOnlyMixin, DeleteView):
    model = Organizer
    template_name = 'festapp/entity_confirm_delete.html'
    success_url = reverse_lazy('organizer_list')
