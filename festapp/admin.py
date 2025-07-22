from django.contrib import admin
from .models import Department, Student, Venue, Event, Registration, Winner, Organizer

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hod_name')
    search_fields = ('name', 'hod_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll_number', 'email', 'department')
    search_fields = ('name', 'roll_number', 'email')
    list_filter = ('department',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'capacity')
    search_fields = ('name', 'location')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'venue', 'department')
    search_fields = ('title',)
    list_filter = ('date', 'department')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'event', 'registered_on')
    search_fields = ('student__name', 'event__title')
    list_filter = ('event',)


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'event', 'position')
    search_fields = ('student__name', 'event__title')
    list_filter = ('position',)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'event')
    search_fields = ('name', 'phone')
    list_filter = ('event',)
