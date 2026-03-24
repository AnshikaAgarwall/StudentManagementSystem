from django.db import models
from django.contrib.auth.models import User
class StudentClass(models.Model):
    class_name = models.CharField(max_length=50) # e.g., "MCA Final"
    section = models.CharField(max_length=10, default="A")
    # Link the class to a Teacher (Staff User)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})

    def __str__(self):
        return f"{self.class_name} - {self.section}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # NEW: Link student to a specific class
    assigned_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    fees_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False, verbose_name="Present")
class Mark(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    internal_marks = models.IntegerField(default=0, null=True, blank=True)
    external_marks = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - Marks"

class Assignment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    # Changed from 'status' choices to a simple Yes/No (Boolean)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - Assignment"