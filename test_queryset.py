import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
django.setup()

from students.models import User, StudentClass, StudentProfile

u = User.objects.filter(username='teacher4').first()
print("Teacher:", u)
my_classes = StudentClass.objects.filter(teacher=u)
current_class = my_classes.first()
print("Current Class:", current_class)

if current_class:
    students = StudentProfile.objects.filter(assigned_class=current_class)
    print("Students in class:", [str(s) for s in students])
else:
    print("No class found!")
