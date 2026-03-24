import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
django.setup()

from django.contrib.auth.models import User, Group
from students.models import StudentProfile, Mark, Assignment

def run_setup():
    # 1. Create Teacher Group
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')

    # 2. Create 4 Teachers
    for i in range(1, 5):
        username = f'teacher{i}'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password='password123', is_staff=True)
            user.groups.add(teacher_group)
            print(f"Created Teacher: {username}")

    # 3. Create 2 Admins (Superusers)
    for i in range(1, 3):
        username = f'admin_user{i}'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password='password123', email=f'admin{i}@sms.com')
            print(f"Created Admin: {username}")

    # 4. Create 5 Students with Profiles & Marks
    student_data = [
        ('Anshika', 'MCA/001', 95, True),
        ('Shivam', 'MCA/002', 88, False),
        ('Rahul', 'MCA/003', 76, True),
        ('Sneha', 'MCA/004', 92, True),
        ('Vikram', 'MCA/005', 65, False),
    ]

    for name, roll, score, paid in student_data:
        if not User.objects.filter(username=name.lower()).exists():
            user = User.objects.create_user(username=name.lower(), password='password123')
            profile = StudentProfile.objects.create(user=user, roll_number=roll, fees_paid=paid, department='MCA')
            Mark.objects.create(student=profile, subject='Python Django', score=score)
            Assignment.objects.create(student=profile, title='Django Project 1', status='S')
            print(f"Created Student: {name}")

if __name__ == "__main__":
    run_setup()
    print("--- Setup Complete! ---")