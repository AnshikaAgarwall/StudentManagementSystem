from django.contrib import admin
from .models import StudentProfile, Attendance, Mark, Assignment, StudentClass

# This tells Django Admin to show your tables
admin.site.register(StudentProfile)
admin.site.register(Attendance)
admin.site.register(Mark)
admin.site.register(Assignment)
admin.site.register(StudentClass)