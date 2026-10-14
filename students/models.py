from django.db import models
from django.contrib.auth.models import User

class StudentClass(models.Model):
    """Represents an academic class and section assigned to a faculty teacher."""
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, default="A")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Student Classes"
        ordering = ['class_name', 'section']

    def __str__(self):
        return f"{self.class_name} - {self.section}"


class StudentProfile(models.Model):
    """Extended profile for students linked to a Django User and assigned class."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    fees_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.roll_number})"


class Attendance(models.Model):
    """Daily attendance record for each student."""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False, verbose_name="Present")

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        status_str = "Present" if self.status else "Absent"
        return f"{self.student.user.username} - {self.date} ({status_str})"


class Mark(models.Model):
    """Internal and external semester examination scores."""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    internal_marks = models.IntegerField(default=0, null=True, blank=True)
    external_marks = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - Marks"


class Assignment(models.Model):
    """Legacy coursework completion status tracker."""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - Assignment"


class ClassAssignment(models.Model):
    """Classroom coursework assigned by teacher with optional reference materials."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reference_file = models.FileField(upload_to='assignments/materials/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.assigned_class})"


class StudentSubmission(models.Model):
    """Uploaded PDF/Word documents submitted by students for an assignment."""
    assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='assignments/submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"