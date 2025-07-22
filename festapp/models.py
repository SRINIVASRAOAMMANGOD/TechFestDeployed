from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    hod_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()

    class Meta:
        db_table = 'venue'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.title


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registration'
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student} registered for {self.event}"


class Winner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        db_table = 'winner'
        unique_together = ('event', 'student')

    def __str__(self):
        return f"{self.student} won position {self.position} in {self.event}"


class Organizer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'organizer'

    def __str__(self):
        return f"{self.name} - {self.event.title}"
