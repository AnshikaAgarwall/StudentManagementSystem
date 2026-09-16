import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
django.setup()

from django.contrib.auth.models import User
from students.models import StudentClass, StudentProfile, Mark, Assignment

def generate_mba():
    print("Generating MBA Students...")

    # 1. Grab Teacher 1
    teacher1_name = "teacher1"
    teacher1 = User.objects.filter(username=teacher1_name).first()
    
    if not teacher1:
        print(f"Teacher '{teacher1_name}' was not found. Please ensure they exist.")
        return

    # 2. Create the MBA Class attached to Teacher 1
    mba_class, created = StudentClass.objects.get_or_create(
        class_name="MBA Section A",
        section="A",
        defaults={'teacher': teacher1}
    )
    if created:
        print(f"Created Class: {mba_class.class_name} mapped to {teacher1.username}")
    else:
        mba_class.teacher = teacher1
        mba_class.save()
        print(f"Mapped existing Class {mba_class.class_name} to {teacher1.username}")

    # 3. Create New Distinct MBA Students
    mba_students = [
        ('Kavya', 'MBA/001', 85, True),
        ('Rohan', 'MBA/002', 76, False),
        ('Aman', 'MBA/003', 92, True),
        ('Neha', 'MBA/004', 68, False),
        ('Priya', 'MBA/005', 88, True),
        ('Arjun', 'MBA/006', 74, True)
    ]

    for name, roll, score, paid in mba_students:
        username = name.lower()
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password='password123')
            profile = StudentProfile.objects.create(
                user=user, 
                roll_number=roll, 
                department='MBA', 
                fees_paid=paid,
                assigned_class=mba_class
            )
            
            # Split their score arbitrarily across internal/external marks logically
            internal = score // 3
            external = score - internal
            
            Mark.objects.create(student=profile, internal_marks=internal, external_marks=external)
            Assignment.objects.create(student=profile, is_submitted=paid)  # Just using 'paid' as a random True/False value
            print(f"Created MBA Student: {name}")

    print("\n--- MBA Data Generation Complete! ---")
    print(f"Log in as '{teacher1.username}' with 'password123' to see your new MBA dashboard populate immediately.")

if __name__ == "__main__":
    generate_mba()
