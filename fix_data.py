import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
django.setup()

from django.contrib.auth.models import User
from students.models import StudentClass, StudentProfile

def fix_database():
    print("Fixing database relationships...")
    
    # 1. Check if teacher4 exists
    teacher4 = User.objects.filter(username='teacher4').first()
    if not teacher4:
        print("Teacher 4 not found! Make sure you created them.")
        return

    # 2. Create an MCA Class assigned to teacher4
    mca_class, created = StudentClass.objects.get_or_create(
        class_name="MCA Final Year",
        section="A",
        defaults={'teacher': teacher4}
    )
    if created:
        print(f"Created Class: {mca_class.class_name} ({mca_class.section}) mapped to teacher4")
    else:
        # If it exists, make sure it's assigned to teacher4
        mca_class.teacher = teacher4
        mca_class.save()
        print(f"Found existing Class: {mca_class.class_name} mapped to teacher4")

    # 3. Assign all existing students to this class
    students_updated = 0
    for profile in StudentProfile.objects.all():
        profile.assigned_class = mca_class
        profile.save()
        students_updated += 1
        print(f"Assigned student '{profile.user.username}' to MCA Final Year")
        
    print(f"\n--- Success! Updated {students_updated} students. ---")
    print("Refresh your teacher dashboard and the students will appear!")

if __name__ == "__main__":
    fix_database()
