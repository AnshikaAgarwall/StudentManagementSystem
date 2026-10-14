import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User, Group
from students.models import (
    StudentClass, StudentProfile, Mark,
    Assignment, Attendance, ClassAssignment, StudentSubmission
)

def reset_and_seed_database():
    """
    Complete Database Reset and Realistic Seeder.
    Wipes previous test data and creates a realistic multi-class, multi-teacher university environment.
    """
    print("==================================================")
    print("🌱 RESETTING & SEEDING UNIVERSITY MANAGEMENT DATABASE")
    print("==================================================")

    # 1. APPLY DATABASE MIGRATIONS
    print("\n--- 1. Applying database migrations ---")
    call_command('migrate', interactive=False)
    print("✓ Database tables verified and migrated.")

    # 2. CLEAN EXISTING RECORDS
    print("\n--- 2. Resetting previous students, classes, and records ---")
    StudentClass.objects.all().delete()
    User.objects.filter(is_superuser=False, is_staff=False).delete()
    print("✓ Old students and classes wiped cleanly.")

    # 3. CONFIGURE TEACHERS & ADMINS
    print("\n--- 3. Setting up Faculty & Administrator Accounts ---")
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')

    teachers = {}
    for i in range(1, 5):
        uname = f'teacher{i}'
        user, created = User.objects.get_or_create(username=uname, defaults={'is_staff': True})
        user.set_password('password123')
        user.is_staff = True
        user.save()
        user.groups.add(teacher_group)
        teachers[uname] = user

    print(f"✓ Configured 4 Faculty Accounts: {list(teachers.keys())}")

    # Admins
    for i in range(1, 3):
        uname = f'admin_user{i}'
        if not User.objects.filter(username=uname).exists():
            User.objects.create_superuser(username=uname, password='password123', email=f'admin{i}@sms.com')
        else:
            u = User.objects.get(username=uname)
            u.set_password('password123')
            u.save()

    print("✓ Configured 2 Admin Accounts: admin_user1, admin_user2")

    # 4. CREATE CLASSES (MULTIPLE CLASSES PER TEACHER)
    print("\n--- 4. Creating Multiple Classes & Sections per Faculty ---")
    mca_a = StudentClass.objects.create(class_name="MCA", section="A", teacher=teachers['teacher1'])
    mca_b = StudentClass.objects.create(class_name="MCA", section="B", teacher=teachers['teacher1'])
    btech_a = StudentClass.objects.create(class_name="B.Tech CSE", section="A", teacher=teachers['teacher1'])

    mba_a = StudentClass.objects.create(class_name="MBA", section="A", teacher=teachers['teacher2'])
    mba_b = StudentClass.objects.create(class_name="MBA", section="B", teacher=teachers['teacher2'])
    bba_a = StudentClass.objects.create(class_name="BBA", section="A", teacher=teachers['teacher2'])

    btech_b = StudentClass.objects.create(class_name="B.Tech CSE", section="B", teacher=teachers['teacher3'])
    btech_it = StudentClass.objects.create(class_name="B.Tech IT", section="A", teacher=teachers['teacher3'])

    bca_a = StudentClass.objects.create(class_name="BCA", section="A", teacher=teachers['teacher4'])
    mca_c = StudentClass.objects.create(class_name="MCA", section="C", teacher=teachers['teacher4'])

    print("✓ Created 10 realistic class sections across MCA, MBA, B.Tech, BBA, and BCA.")

    # 5. ENROLL STUDENTS WITH REALISTIC DIVERSE DATA
    print("\n--- 5. Enrolling Students with Complete Records ---")
    student_roster = [
        # (Name, Roll, Dept, Class, FeesPaid, InternalMarks, ExternalMarks, AssignmentSubmitted, AttendancePattern)
        ('Anshika', 'MCA/2026/01', 'MCA', mca_a, True, 28, 65, True, 'excellent'),
        ('Rahul', 'MCA/2026/02', 'MCA', mca_a, True, 22, 54, True, 'average'),
        ('Sneha', 'MCA/2026/03', 'MCA', mca_a, False, 26, 58, True, 'excellent'),
        ('Karan', 'MCA/2026/04', 'MCA', mca_a, False, 14, 32, False, 'defaulter'),

        ('Vikram', 'MCA/2026/11', 'MCA', mca_b, True, 25, 60, True, 'excellent'),
        ('Shivam', 'MCA/2026/12', 'MCA', mca_b, False, 20, 48, False, 'average'),
        ('Pooja', 'MCA/2026/13', 'MCA', mca_b, True, 27, 62, True, 'excellent'),

        ('Aditya', 'BT/CS/001', 'B.Tech', btech_a, True, 29, 68, True, 'excellent'),
        ('Tanvi', 'BT/CS/002', 'B.Tech', btech_a, True, 21, 50, True, 'average'),
        ('Harsh', 'BT/CS/003', 'B.Tech', btech_a, False, 12, 28, False, 'defaulter'),

        ('Kavya', 'MBA/2026/01', 'MBA', mba_a, True, 27, 63, True, 'excellent'),
        ('Rohan', 'MBA/2026/02', 'MBA', mba_a, False, 19, 45, True, 'average'),
        ('Aman', 'MBA/2026/03', 'MBA', mba_a, True, 24, 56, True, 'average'),

        ('Neha', 'MBA/2026/11', 'MBA', mba_b, True, 28, 64, True, 'excellent'),
        ('Priya', 'MBA/2026/12', 'MBA', mba_b, True, 23, 52, False, 'average'),
        ('Arjun', 'MBA/2026/13', 'MBA', mba_b, False, 15, 30, False, 'defaulter'),

        ('Simran', 'BBA/2026/01', 'BBA', bba_a, True, 25, 55, True, 'excellent'),
        ('Varun', 'BBA/2026/02', 'BBA', bba_a, True, 18, 42, False, 'defaulter'),

        ('Mohit', 'BT/CS/051', 'B.Tech', btech_b, True, 26, 61, True, 'excellent'),
        ('Rhea', 'BT/CS/052', 'B.Tech', btech_b, False, 22, 53, True, 'average'),

        ('Ishaan', 'BT/IT/001', 'B.Tech', btech_it, True, 28, 66, True, 'excellent'),
        ('Ananya', 'BT/IT/002', 'B.Tech', btech_it, True, 24, 57, True, 'average'),

        ('Sameer', 'BCA/2026/01', 'BCA', bca_a, True, 23, 50, True, 'average'),
        ('Divya', 'BCA/2026/02', 'BCA', bca_a, False, 11, 25, False, 'defaulter'),

        ('Deepak', 'MCA/2026/21', 'MCA', mca_c, True, 27, 60, True, 'excellent'),
        ('Megha', 'MCA/2026/22', 'MCA', mca_c, True, 20, 47, True, 'average'),
    ]

    today = date.today()
    past_dates = [today - timedelta(days=i) for i in range(1, 8)]

    created_students = []

    for name, roll, dept, target_class, fees, internal, external, assign_sub, pattern in student_roster:
        username = name.lower()
        user = User.objects.create_user(username=username, password='password123')

        profile = StudentProfile.objects.create(
            user=user,
            roll_number=roll,
            department=dept,
            fees_paid=fees,
            assigned_class=target_class
        )

        Mark.objects.create(
            student=profile,
            internal_marks=internal,
            external_marks=external
        )

        Assignment.objects.create(
            student=profile,
            is_submitted=assign_sub
        )

        for d in past_dates:
            if pattern == 'excellent':
                is_p = (random.random() > 0.08)
            elif pattern == 'average':
                is_p = (random.random() > 0.22)
            else:
                is_p = (random.random() > 0.55)

            Attendance.objects.create(student=profile, date=d, status=is_p)

        created_students.append(profile)

    print(f"✓ Created {len(created_students)} Students with complete marks, fee status, and 7-day attendance histories.")

    # 6. PUBLISH CLASS ASSIGNMENTS
    print("\n--- 6. Publishing Coursework Assignments ---")
    ClassAssignment.objects.all().delete()

    ClassAssignment.objects.create(
        title="Django REST Framework & Secure Auth",
        description="Build a REST API endpoint for student enrollment with token-based authentication. Submit report in PDF or Word format.",
        assigned_class=mca_a,
        teacher=teachers['teacher1'],
        due_date=today + timedelta(days=5)
    )

    ClassAssignment.objects.create(
        title="Data Structures: Binary Trees & Graph Traversal",
        description="Implement BFS and DFS algorithms in C++ or Python. Include test cases and time complexity analysis in your submitted document.",
        assigned_class=btech_a,
        teacher=teachers['teacher1'],
        due_date=today + timedelta(days=7)
    )

    ClassAssignment.objects.create(
        title="Strategic Marketing & Brand Equity Case Study",
        description="Analyze a real-world FMCG company brand repositioning strategy. Submit a structured 3-5 page docx/pdf paper.",
        assigned_class=mba_a,
        teacher=teachers['teacher2'],
        due_date=today + timedelta(days=4)
    )

    print("✓ Published 3 active assignments across MCA, B.Tech CSE, and MBA sections.")
    print("\n==================================================")
    print("🎉 UNIVERSITY DATABASE SUCCESSFULLY SEEDED!")
    print("==================================================")

if __name__ == '__main__':
    reset_and_seed_database()
