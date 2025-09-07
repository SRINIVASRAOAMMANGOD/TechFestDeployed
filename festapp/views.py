from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection, IntegrityError
from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from .models import Winner  # Import Winner model
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import Department, Student, Venue, Event, Registration, Winner, Organizer
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")

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


# =======================
# Department
# =======================
# @login_required
def department_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, hod_name FROM department ORDER BY name")
        departments = cursor.fetchall()
    return render(request, "festapp/department_list.html", {"departments": departments})


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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



@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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



@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
def registration_delete(request, pk):
    return safe_delete(request, "festapp", "Registration", pk, "registration_list", "registration")
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(is_admin)
def registration_delete(request, pk):
    return safe_delete(request, "festapp", "Registration", pk, "registration_list", "registration")

@login_required
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
def organizer_delete(request, pk):
    return safe_delete(request, "festapp", "Organizer", pk, "organizer_list", "organizer")
