from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection, IntegrityError
from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from .models import Winner  # Import Winner model
import csv
import io
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Department, Student, Venue, Event, Registration, Winner, Organizer
from .forms import CSVUploadForm

# =======================
# Health Check
# =======================
def health_check(request):
    """Simple health check endpoint for deployment monitoring"""
    return JsonResponse({"status": "ok", "message": "Application is running"})

def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get("model")
        if not model_name:
            return render(request, "festapp/export_data.html", {"error": "Please select a model."})

        model_map = {
            "Department": Department,
            "Student": Student,
            "Venue": Venue,
            "Event": Event,
            "Registration": Registration,
            "Winner": Winner,
            "Organizer": Organizer,
        }

        Model = model_map.get(model_name)
        if not Model:
            return render(request, "festapp/export_data.html", {"error": "Invalid model selected."})

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{model_name}.csv"'
        writer = csv.writer(response)

        # Handle each model separately
        if model_name == "Department":
            writer.writerow(["ID", "Name", "HOD Name"])
            for d in Model.objects.all():
                writer.writerow([d.id, d.name, d.hod_name])

        elif model_name == "Student":
            writer.writerow(["ID", "Name", "Roll Number", "Email", "Department"])
            for s in Model.objects.all():
                writer.writerow([s.id, s.name, s.roll_number, s.email, s.department.name if s.department else ""])

        elif model_name == "Venue":
            writer.writerow(["ID", "Name", "Location", "Capacity"])
            for v in Model.objects.all():
                writer.writerow([v.id, v.name, v.location, v.capacity])

        elif model_name == "Event":
            writer.writerow(["ID", "Title", "Description", "Date", "Venue", "Department"])
            for e in Model.objects.all():
                writer.writerow([
                    e.id, e.title, e.description,
                    e.date.strftime("%Y-%m-%d") if e.date else "",
                    e.venue.name if e.venue else "",
                    e.department.name if e.department else ""
                ])

        elif model_name == "Registration":
            writer.writerow(["ID", "Student", "Event", "Registered On"])
            for r in Model.objects.all():
                writer.writerow([
                    r.id,
                    r.student.name if r.student else "",
                    r.event.title if r.event else "",
                    r.registered_on.strftime("%Y-%m-%d %H:%M:%S") if r.registered_on else ""
                ])

        elif model_name == "Winner":
            writer.writerow(["ID", "Event", "Student", "Position"])
            for w in Model.objects.all():
                writer.writerow([
                    w.id,
                    w.event.title if w.event else "",
                    w.student.name if w.student else "",
                    w.position
                ])

        elif model_name == "Organizer":
            writer.writerow(["ID", "Name", "Phone", "Event"])
            for o in Model.objects.all():
                writer.writerow([
                    o.id, o.name, o.phone,
                    o.event.title if o.event else ""
                ])

        return response

    return render(request, "festapp/export_data.html")


# =======================
# Index
# =======================
@login_required
def index(request):
    return render(request, "festapp/index.html")


# =======================
# Generic safe delete
# =======================
# def safe_delete(request, app_label, model_name, pk, success_url_name, object_name="object"):
#     """Generic safe delete handler for all models."""
#     Model = apps.get_model(app_label, model_name)
#     obj = get_object_or_404(Model, pk=pk)

#     if request.method == "POST":
#         try:
#             obj.delete()
#             messages.success(request, f"{model_name} deleted successfully")
#             return redirect(success_url_name)
#         except IntegrityError:
#             return render(request, "festapp/delete_error.html", {
#                 "object": obj,
#                 "reason": f"This {model_name} cannot be deleted because related records exist."
#             })

#     return render(request, "festapp/confirm_delete.html", {object_name: obj})
def safe_delete(request, app_label, model_name, pk, success_url, object_name):
    Model = apps.get_model(app_label, model_name)
    obj = Model.objects.get(pk=pk)

    # Check if related objects exist (simulate PROTECT behavior)
    protected_relations = []
    for rel in obj._meta.related_objects:
        if rel.related_model.objects.filter(**{rel.field.name: obj}).exists():
            protected_relations.append(rel.related_model.__name__)

    if protected_relations:
        return render(request, "festapp/delete_error.html", {
            "object": obj,
            "reason": f"Cannot delete {object_name} because it is referenced by: {', '.join(protected_relations)}"
        })

    obj.delete()
    return redirect(success_url)

# =======================
# Authentication
# =======================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        return render(request, "festapp/login.html", {"error": "Invalid credentials"})
    return render(request, "festapp/login.html")


def user_logout(request):
    logout(request)
    return redirect("index")


def is_admin(user):
    return user.is_superuser or user.is_staff


def can_edit(user):
    """Allow both admins and general users to perform CRUD operations"""
    return user.is_superuser or user.is_staff or user.groups.filter(name='GeneralUsers').exists()


# =======================
# Department
# =======================
# @login_required
def department_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, hod_name FROM department ORDER BY name")
        departments = cursor.fetchall()
    return render(request, "festapp/department_list.html", {"departments": departments})


@user_passes_test(can_edit)
def department_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        hod_name = request.POST.get("hod_name")
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO department (name, hod_name) VALUES (%s, %s)", [name, hod_name])
            return redirect("department_list")
        except Exception as e:
            return render(request, "festapp/department_form.html", {"error": str(e)})
    return render(request, "festapp/department_form.html")


@user_passes_test(can_edit)
def department_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, hod_name FROM department WHERE id=%s", [pk])
        department = cursor.fetchone()

    if request.method == "POST":
        name = request.POST.get("name", department[1])
        hod_name = request.POST.get("hod_name", department[2])

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE department SET name=%s, hod_name=%s WHERE id=%s",
                [name, hod_name, pk]
            )
        messages.success(request, "Department updated successfully")
        return redirect("department_list")

    return render(request, "festapp/department_form.html", {"department": department})



@user_passes_test(can_edit)
def department_delete(request, pk):
    return safe_delete(request, "festapp", "Department", pk, "department_list", "department")


# =======================
# Student
# =======================
# @login_required
def student_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.id, s.name, s.roll_number, s.email, d.name as department_name 
            FROM student s
            LEFT JOIN department d ON s.department_id = d.id
            ORDER BY s.name
        """)
        students = cursor.fetchall()
    return render(request, "festapp/student_list.html", {"students": students})


@user_passes_test(can_edit)
def student_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        roll_number = request.POST.get("roll_number")
        email = request.POST.get("email")
        department_id = request.POST.get("department_id")

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM student WHERE roll_number = %s", [roll_number])
                if cursor.fetchone():
                    messages.error(request, "Roll number already exists")
                    raise Exception("Roll number already exists")
                cursor.execute(
                    "INSERT INTO student (name, roll_number, email, department_id) VALUES (%s, %s, %s, %s)",
                    [name, roll_number, email, department_id]
                )
            messages.success(request, "Student added successfully")
            return redirect("student_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM department ORDER BY name")
        departments = cursor.fetchall()
    return render(request, "festapp/student_form.html", {"departments": departments})


@user_passes_test(can_edit)
def student_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, roll_number, email, department_id FROM student WHERE id=%s", [pk])
        student = cursor.fetchone()
        cursor.execute("SELECT id, name FROM department ORDER BY name")
        departments = cursor.fetchall()

    if request.method == "POST":
        name = request.POST.get("name", student[1])
        roll_number = request.POST.get("roll_number", student[2])
        email = request.POST.get("email", student[3])
        department_id = request.POST.get("department_id", student[4])

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE student SET name=%s, roll_number=%s, email=%s, department_id=%s WHERE id=%s",
                [name, roll_number, email, department_id, pk]
            )
        messages.success(request, "Student updated successfully")
        return redirect("student_list")

    return render(request, "festapp/student_form.html", {"student": student, "departments": departments})



@user_passes_test(can_edit)
def student_delete(request, pk):
    return safe_delete(request, "festapp", "Student", pk, "student_list", "student")


# =======================
# Venue
# =======================
# @login_required
def venue_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, location, capacity FROM venue ORDER BY name")
        venues = cursor.fetchall()
    return render(request, "festapp/venue_list.html", {"venues": venues})


@user_passes_test(can_edit)
def venue_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        capacity = request.POST.get("capacity")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO venue (name, location, capacity) VALUES (%s, %s, %s)",
                    [name, location, capacity]
                )
            messages.success(request, "Venue added successfully")
            return redirect("venue_list")
        except Exception as e:
            messages.error(request, str(e))
    return render(request, "festapp/venue_form.html")


@user_passes_test(can_edit)
def venue_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, location, capacity FROM venue WHERE id=%s", [pk])
        venue = cursor.fetchone()

    if request.method == "POST":
        name = request.POST.get("name", venue[1])
        location = request.POST.get("location", venue[2])
        capacity = request.POST.get("capacity", venue[3])

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE venue SET name=%s, location=%s, capacity=%s WHERE id=%s",
                [name, location, capacity, pk]
            )
        messages.success(request, "Venue updated successfully")
        return redirect("venue_list")

    return render(request, "festapp/venue_form.html", {"venue": venue})


@user_passes_test(can_edit)
def venue_delete(request, pk):
    return safe_delete(request, "festapp", "Venue", pk, "venue_list", "venue")


# =======================
# Event
# =======================
# @login_required
def event_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.id, e.title, e.description, e.date, 
                   v.name as venue_name, d.name as department_name
            FROM event e
            LEFT JOIN venue v ON e.venue_id = v.id
            LEFT JOIN department d ON e.department_id = d.id
            ORDER BY e.date DESC
        """)
        events = cursor.fetchall()
    return render(request, "festapp/event_list.html", {"events": events})


@login_required
@user_passes_test(can_edit)
def event_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        venue_id = request.POST.get("venue_id")
        department_id = request.POST.get("department_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO event (title, description, date, venue_id, department_id) VALUES (%s, %s, %s, %s, %s)",
                    [title, description, date, venue_id, department_id]
                )
            messages.success(request, "Event added successfully")
            return redirect("event_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, capacity FROM venue ORDER BY name")
        venues = cursor.fetchall()
        cursor.execute("SELECT id, name FROM department ORDER BY name")
        departments = cursor.fetchall()
    return render(request, "festapp/event_form.html", {"venues": venues, "departments": departments})


@login_required
@user_passes_test(can_edit)
def event_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, description, date, venue_id, department_id FROM event WHERE id=%s", [pk])
        event = cursor.fetchone()
        cursor.execute("SELECT id, name FROM venue ORDER BY name")
        venues = cursor.fetchall()
        cursor.execute("SELECT id, name FROM department ORDER BY name")
        departments = cursor.fetchall()

    if request.method == "POST":
        title = request.POST.get("title", event[1])
        description = request.POST.get("description", event[2])
        date = request.POST.get("date", event[3])
        venue_id = request.POST.get("venue_id", event[4])
        department_id = request.POST.get("department_id", event[5])

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE event SET title=%s, description=%s, date=%s, venue_id=%s, department_id=%s WHERE id=%s",
                [title, description, date, venue_id, department_id, pk]
            )
        messages.success(request, "Event updated successfully")
        return redirect("event_list")

    return render(request, "festapp/event_form.html", {"event": event, "venues": venues, "departments": departments})



@login_required
@user_passes_test(can_edit)
def event_delete(request, pk):
    return safe_delete(request, "festapp", "Event", pk, "event_list", "event")


# =======================
# Registration
# =======================
# @login_required
def registration_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id, e.title, s.name, s.roll_number, r.registered_on
            FROM registration r
            JOIN event e ON r.event_id = e.id
            JOIN student s ON r.student_id = s.id
            ORDER BY r.registered_on DESC
        """)
        registrations = cursor.fetchall()
    return render(request, "festapp/registration_list.html", {"registrations": registrations})
# =======================
# Registration Update
# =======================
@login_required
@user_passes_test(can_edit)
def registration_update(request, pk):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student_id = request.POST.get("student_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE registration SET event_id=%s, student_id=%s WHERE id=%s",
                    [event_id, student_id, pk]
                )
                messages.success(request, "Registration updated successfully")
                return redirect("registration_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, event_id, student_id FROM registration WHERE id=%s", [pk])
        registration = cursor.fetchone()
        cursor.execute("SELECT id, title FROM event ORDER BY date")
        events = cursor.fetchall()
        cursor.execute("SELECT id, name, roll_number FROM student")
        students = cursor.fetchall()
    return render(request, "festapp/registration_form.html", {
        "registration": registration, "events": events, "students": students
    })


# =======================
# Winner Update
# =======================
@login_required
@user_passes_test(can_edit)
def winner_update(request, pk):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student_id = request.POST.get("student_id")
        position = int(request.POST.get("position"))

        if position not in [1, 2, 3]:
            messages.error(request, "Position must be 1, 2 or 3")
            return redirect("winner_list")

        try:
            if Winner.objects.filter(event_id=event_id, position=position).exclude(pk=pk).exists():
                messages.error(request, f"Position {position} already awarded for this event")
                return redirect("winner_list")
            Winner.objects.filter(pk=pk).update(event_id=event_id, student_id=student_id, position=position)
            messages.success(request, "Winner updated successfully")
            return redirect("winner_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, event_id, student_id, position FROM winner WHERE id=%s", [pk])
        winner = cursor.fetchone()
        cursor.execute("SELECT id, title FROM event ORDER BY date DESC")
        events = cursor.fetchall()
        cursor.execute("SELECT id, name, roll_number FROM student")
        students = cursor.fetchall()
    return render(request, "festapp/winner_form.html", {
        "winner": winner, "events": events, "students": students
    })


@login_required
def registration_create(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student_id = request.POST.get("student_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM registration WHERE event_id=%s AND student_id=%s", [event_id, student_id])
                if cursor.fetchone():
                    messages.error(request, "Student already registered for this event")
                    return redirect("registration_list")
                cursor.execute(
                    "INSERT INTO registration (event_id, student_id, registered_on) VALUES (%s, %s, %s)",
                    [event_id, student_id, timezone.now()]
                )
                messages.success(request, "Registration successful")
                return redirect("registration_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title FROM event ORDER BY date")
        events = cursor.fetchall()
        cursor.execute("SELECT id, name, roll_number FROM student")
        students = cursor.fetchall()
    return render(request, "festapp/registration_form.html", {"events": events, "students": students})


@login_required
@user_passes_test(can_edit)
def registration_delete(request, pk):
    return safe_delete(request, "festapp", "Registration", pk, "registration_list", "registration")
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(can_edit)
def registration_delete(request, pk):
    return safe_delete(request, "festapp", "Registration", pk, "registration_list", "registration")

@login_required
@user_passes_test(can_edit)
def registration_update(request, pk):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student_id = request.POST.get("student_id")
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE registration SET event_id=%s, student_id=%s WHERE id=%s",
                [event_id, student_id, pk]
            )
        messages.success(request, "Registration updated successfully")
        return redirect("registration_list")

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, event_id, student_id FROM registration WHERE id=%s", [pk])
        registration = cursor.fetchone()
        cursor.execute("SELECT id, title FROM event ORDER BY date")
        events = cursor.fetchall()
        cursor.execute("SELECT id, name, roll_number FROM student")
        students = cursor.fetchall()
    return render(request, "festapp/registration_form.html", {"registration": registration, "events": events, "students": students})


# =======================
# Winner
# =======================
# @login_required
def winner_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT w.id, e.title, s.name, s.roll_number, w.position 
            FROM winner w
            JOIN event e ON w.event_id = e.id
            JOIN student s ON w.student_id = s.id
            ORDER BY e.date DESC, w.position
        """)
        winners = cursor.fetchall()
    return render(request, "festapp/winner_list.html", {"winners": winners})


@login_required
@user_passes_test(can_edit)
def winner_create(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student_id = request.POST.get("student_id")
        position = int(request.POST.get("position"))

        if position not in [1, 2, 3]:
            messages.error(request, "Position must be 1, 2 or 3")
            return redirect("winner_list")

        try:
            if Winner.objects.filter(event_id=event_id, position=position).exists():
                messages.error(request, f"Position {position} already awarded for this event")
                return redirect("winner_list")
            Winner.objects.create(event_id=event_id, student_id=student_id, position=position)
            messages.success(request, "Winner added successfully")
            return redirect("winner_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title FROM event ORDER BY date DESC")
        events = cursor.fetchall()
        cursor.execute("SELECT id, name, roll_number FROM student")
        students = cursor.fetchall()
    return render(request, "festapp/winner_form.html", {"events": events, "students": students})


@login_required
@user_passes_test(can_edit)
def winner_delete(request, pk):
    return safe_delete(request, "festapp", "Winner", pk, "winner_list", "winner")


# =======================
# Organizer
# =======================
# @login_required
def organizer_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.id, o.name, o.phone, e.title
            FROM organizer o
            JOIN event e ON o.event_id = e.id
            ORDER BY e.date DESC
        """)
        organizers = cursor.fetchall()
    return render(request, "festapp/organizer_list.html", {"organizers": organizers})


@login_required
@user_passes_test(can_edit)
def organizer_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        event_id = request.POST.get("event_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO organizer (name, phone, event_id) VALUES (%s, %s, %s)", [name, phone, event_id])
                messages.success(request, "Organizer added successfully")
                return redirect("organizer_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title FROM event ORDER BY date DESC")
        events = cursor.fetchall()
    return render(request, "festapp/organizer_form.html", {"events": events})


@login_required
@user_passes_test(can_edit)
def organizer_update(request, pk):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        event_id = request.POST.get("event_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE organizer SET name=%s, phone=%s, event_id=%s WHERE id=%s",
                    [name, phone, event_id, pk]
                )
                messages.success(request, "Organizer updated successfully")
                return redirect("organizer_list")
        except Exception as e:
            messages.error(request, str(e))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, phone, event_id FROM organizer WHERE id=%s", [pk])
        organizer = cursor.fetchone()
        cursor.execute("SELECT id, title FROM event ORDER BY date DESC")
        events = cursor.fetchall()
    return render(request, "festapp/organizer_form.html", {"organizer": organizer, "events": events})


@login_required
@user_passes_test(can_edit)
def organizer_delete(request, pk):
    return safe_delete(request, "festapp", "Organizer", pk, "organizer_list", "organizer")


# =======================
# CSV Import Functionality
# =======================
@login_required
@user_passes_test(can_edit)
def csv_import(request):
    """Main CSV import page to select model type"""
    return render(request, 'festapp/csv_import.html')


@login_required
@user_passes_test(can_edit)
def import_department_csv(request):
    """Import departments from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_department_csv')
            
            try:
                # Read CSV file
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        Department.objects.create(
                            name=row['name'],
                            hod_name=row['hod_name']
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} departments')
                if error_count > 0:
                    for error in errors[:5]:  # Show first 5 errors
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('department_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_department_csv')
    else:
        form = CSVUploadForm()
    
    # CSV format example
    csv_format = "name,hod_name\nComputer Science,Dr. Smith\nElectronics,Dr. Johnson"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Department',
        'csv_format': csv_format,
        'fields': 'name, hod_name'
    })


@login_required
@user_passes_test(can_edit)
def import_student_csv(request):
    """Import students from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_student_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        department = Department.objects.get(name=row['department'])
                        Student.objects.create(
                            name=row['name'],
                            roll_number=row['roll_number'],
                            email=row['email'],
                            department=department
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} students')
                if error_count > 0:
                    for error in errors[:5]:
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('student_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_student_csv')
    else:
        form = CSVUploadForm()
    
    csv_format = "name,roll_number,email,department\nJohn Doe,CS001,john@example.com,Computer Science\nJane Smith,CS002,jane@example.com,Electronics"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Student',
        'csv_format': csv_format,
        'fields': 'name, roll_number, email, department (department name must exist)'
    })


@login_required
@user_passes_test(can_edit)
def import_venue_csv(request):
    """Import venues from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_venue_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        Venue.objects.create(
                            name=row['name'],
                            location=row['location'],
                            capacity=int(row['capacity'])
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} venues')
                if error_count > 0:
                    for error in errors[:5]:
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('venue_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_venue_csv')
    else:
        form = CSVUploadForm()
    
    csv_format = "name,location,capacity\nMain Hall,Building A,500\nAuditorium,Building B,1000"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Venue',
        'csv_format': csv_format,
        'fields': 'name, location, capacity (integer)'
    })


@login_required
@user_passes_test(can_edit)
def import_event_csv(request):
    """Import events from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_event_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        venue = Venue.objects.get(name=row['venue']) if row.get('venue') else None
                        department = Department.objects.get(name=row['department'])
                        
                        Event.objects.create(
                            title=row['title'],
                            description=row['description'],
                            date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                            venue=venue,
                            department=department
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} events')
                if error_count > 0:
                    for error in errors[:5]:
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('event_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_event_csv')
    else:
        form = CSVUploadForm()
    
    csv_format = "title,description,date,venue,department\nCoding Contest,Programming competition,2025-10-25,Main Hall,Computer Science\nRobotics,Robot building event,2025-10-26,Auditorium,Electronics"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Event',
        'csv_format': csv_format,
        'fields': 'title, description, date (YYYY-MM-DD), venue (optional, must exist), department (must exist)'
    })


@login_required
@user_passes_test(can_edit)
def import_registration_csv(request):
    """Import registrations from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_registration_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        student = Student.objects.get(roll_number=row['student_roll_number'])
                        event = Event.objects.get(title=row['event_title'])
                        
                        Registration.objects.create(
                            student=student,
                            event=event
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} registrations')
                if error_count > 0:
                    for error in errors[:5]:
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('registration_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_registration_csv')
    else:
        form = CSVUploadForm()
    
    csv_format = "student_roll_number,event_title\nCS001,Coding Contest\nCS002,Robotics"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Registration',
        'csv_format': csv_format,
        'fields': 'student_roll_number (must exist), event_title (must exist)'
    })


@login_required
@user_passes_test(can_edit)
def import_winner_csv(request):
    """Import winners from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_winner_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        event = Event.objects.get(title=row['event_title'])
                        student = Student.objects.get(roll_number=row['student_roll_number'])
                        
                        Winner.objects.create(
                            event=event,
                            student=student,
                            position=int(row['position'])
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} winners')
                if error_count > 0:
                    for error in errors[:5]:
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('winner_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_winner_csv')
    else:
        form = CSVUploadForm()
    
    csv_format = "event_title,student_roll_number,position\nCoding Contest,CS001,1\nCoding Contest,CS002,2"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Winner',
        'csv_format': csv_format,
        'fields': 'event_title (must exist), student_roll_number (must exist), position (integer)'
    })


@login_required
@user_passes_test(can_edit)
def import_organizer_csv(request):
    """Import organizers from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('import_organizer_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                csv_reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        event = Event.objects.get(title=row['event_title'])
                        
                        Organizer.objects.create(
                            name=row['name'],
                            phone=row['phone'],
                            event=event
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} organizers')
                if error_count > 0:
                    for error in errors[:5]:
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('organizer_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                return redirect('import_organizer_csv')
    else:
        form = CSVUploadForm()
    
    csv_format = "name,phone,event_title\nAlice Brown,1234567890,Coding Contest\nBob Wilson,0987654321,Robotics"
    return render(request, 'festapp/csv_import_form.html', {
        'form': form,
        'model_name': 'Organizer',
        'csv_format': csv_format,
        'fields': 'name, phone, event_title (must exist)'
    })

