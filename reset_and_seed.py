import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
django.setup()

from django.contrib.auth.models import User
from students.models import StudentClass, StudentProfile, Mark, Assignment, Attendance

def nuclear_reset_and_seed():
    print("--- 1. CLEANING UP OLD MESSY DATA ---")
    # Delete all previous classes so we don't have duplicates like "mca a", "mca section a"
    StudentClass.objects.all().delete()
    print("Deleted all old StudentClasses.")

    # Delete all old students (this automatically deletes Marks, Attendance, Assignments due to CASCADE)
    old_students = User.objects.filter(is_superuser=False, is_staff=False)
    count = old_students.count()
    old_students.delete()
    print(f"Deleted {count} old Student Profiles to start perfectly fresh.")

    print("\n--- 2. CREATING EXACT CLASSES FOR SPECIFIC TEACHERS ---")
    # Fetch teachers
    t1 = User.objects.filter(username='teacher1').first()
    t2 = User.objects.filter(username='teacher2').first()
    t3 = User.objects.filter(username='teacher3').first()
    t4 = User.objects.filter(username='teacher4').first()

    if not all([t1, t2, t3, t4]):
        print("ERROR: Teachers 1-4 not found. Please run your original setup_data.py first!")
        return

    # Create exactly 4 classes, strictly mapping 1 teacher to 1 section
    mca_a = StudentClass.objects.create(class_name="MCA", section="A", teacher=t1)
    mca_b = StudentClass.objects.create(class_name="MCA", section="B", teacher=t2)
    mba_a = StudentClass.objects.create(class_name="MBA", section="A", teacher=t3)
    mba_b = StudentClass.objects.create(class_name="MBA", section="B", teacher=t4)
    print("Created exactly 4 classes: MCA A (teacher1), MCA B (teacher2), MBA A (teacher3), MBA B (teacher4)")

    print("\n--- 3. ADDING STUDENTS ---")
    data = [
        # MCA Section A (Teacher 1)
        ('Anshika', 'MCA_A_001', 'MCA', mca_a),
        ('Rahul', 'MCA_A_002', 'MCA', mca_a),
        ('Sneha', 'MCA_A_003', 'MCA', mca_a),
        
        # MCA Section B (Teacher 2)
        ('Vikram', 'MCA_B_001', 'MCA', mca_b),
        ('Shivam', 'MCA_B_002', 'MCA', mca_b),
        ('Pooja', 'MCA_B_003', 'MCA', mca_b),
        
        # MBA Section A (Teacher 3)
        ('Kavya', 'MBA_A_001', 'MBA', mba_a),
        ('Rohan', 'MBA_A_002', 'MBA', mba_a),
        ('Aman', 'MBA_A_003', 'MBA', mba_a),
        
        # MBA Section B (Teacher 4)
        ('Neha', 'MBA_B_001', 'MBA', mba_b),
        ('Priya', 'MBA_B_002', 'MBA', mba_b),
        ('Arjun', 'MBA_B_003', 'MBA', mba_b),
    ]

    for name, roll, dept, s_class in data:
        username = name.lower()
        # Create fresh user
        user = User.objects.create_user(username=username, password='password123')
        
        # Link user strictly to exactly ONE class
        profile = StudentProfile.objects.create(
            user=user, 
            roll_number=roll, 
            department=dept, 
            fees_paid=True,
            assigned_class=s_class
        )
        
        # Generate default marks out of 100 arbitrarily
        Mark.objects.create(student=profile, internal_marks=20, external_marks=55)
        Assignment.objects.create(student=profile, is_submitted=True)
        print(f"Added Student '{name}' completely isolated into '{s_class.class_name} Section {s_class.section}'")

    print("\n--- ALL DONE! PERFECT SANDBOX READY. ---")
    print("Now, teacher1 will ONLY see MCA A. teacher4 will ONLY see MBA B.")

if __name__ == "__main__":
    nuclear_reset_and_seed()
