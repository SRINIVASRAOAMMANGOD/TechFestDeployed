from django import forms
from .models import Department, Student, Venue, Event, Registration, Winner, Organizer

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'hod_name']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'department']


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'location', 'capacity']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'venue', 'department']


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['student', 'event']


class WinnerForm(forms.ModelForm):
    class Meta:
        model = Winner
        fields = ['event', 'student', 'position']


class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['name', 'phone', 'event']


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV File',
        help_text='Upload a CSV file to import data',
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
