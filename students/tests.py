from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import StudentClass, StudentProfile, Attendance, Mark, ClassAssignment, StudentSubmission

class StudentManagementSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Teacher User
        self.teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        self.teacher_user = User.objects.create_user(
            username='prof_sharma',
            password='password123',
            is_staff=True
        )
        self.teacher_user.groups.add(self.teacher_group)

        # Create Student User & Profile
        self.student_user = User.objects.create_user(
            username='test_student',
            password='password123'
        )
        self.s_class = StudentClass.objects.create(
            class_name="MCA",
            section="A",
            teacher=self.teacher_user
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            roll_number="MCA/TEST/01",
            department="MCA",
            fees_paid=True,
            assigned_class=self.s_class
        )

    def test_login_page_renders(self):
        """Ensure login portal responds with 200 OK."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EduManage Portal")

    def test_student_profile_attributes(self):
        """Verify student profile and class mapping."""
        self.assertEqual(self.student_profile.assigned_class.class_name, "MCA")
        self.assertEqual(self.student_profile.assigned_class.teacher.username, "prof_sharma")
        self.assertTrue(self.student_profile.fees_paid)

    def test_attendance_creation_and_update(self):
        """Test daily attendance record status update."""
        today = date.today()
        att, created = Attendance.objects.update_or_create(
            student=self.student_profile,
            date=today,
            defaults={'status': True}
        )
        self.assertTrue(att.status)

        # Update to False (Absent)
        att, created = Attendance.objects.update_or_create(
            student=self.student_profile,
            date=today,
            defaults={'status': False}
        )
        self.assertFalse(created)
        self.assertFalse(att.status)

    def test_marks_record(self):
        """Test internal and external score creation."""
        mark = Mark.objects.create(
            student=self.student_profile,
            internal_marks=28,
            external_marks=65
        )
        self.assertEqual(mark.internal_marks + mark.external_marks, 93)

    def test_class_assignment_creation(self):
        """Test assignment publishing and relationship with class."""
        assignment = ClassAssignment.objects.create(
            title="Data Structures Lab",
            description="Complete binary tree implementation",
            assigned_class=self.s_class,
            teacher=self.teacher_user,
            due_date=date.today()
        )
        self.assertEqual(assignment.assigned_class.class_name, "MCA")
        self.assertEqual(assignment.teacher.username, "prof_sharma")
