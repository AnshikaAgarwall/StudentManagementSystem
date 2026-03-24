from datetime import date, timedelta # <--- Add this at the top of views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # <--- ADD THIS LINE
from django.contrib.auth.models import User, Group
from .models import StudentProfile, Mark, Assignment, Attendance, StudentClass
@login_required
def dashboard(request):
    user = request.user
    today = date.today()  
    
    # 1. ADMIN CHECK
    if user.is_superuser:
        context = {
            'total_students': StudentProfile.objects.count(),
            'unpaid_fees': StudentProfile.objects.filter(fees_paid=False).count(),
            'students': StudentProfile.objects.all(),
        }
        return render(request, 'admin_dashboard.html', context)

# 2. TEACHER CHECK
    is_teacher = user.groups.filter(name='Teacher').exists() or user.username.startswith('teacher')
    
    if is_teacher:
        # Get only the classes assigned to THIS teacher
        my_classes = StudentClass.objects.filter(teacher=user)
        
        # Get the ID from the dropdown/URL. If none, pick the first class.
        selected_class_id = request.GET.get('class_id')
        
        if selected_class_id:
            students = StudentProfile.objects.filter(assigned_class_id=selected_class_id)
            current_class = StudentClass.objects.get(id=selected_class_id)
        else:
            current_class = my_classes.first()
            students = StudentProfile.objects.filter(assigned_class=current_class) if current_class else []

        context = {
            'students': students,
            'my_classes': my_classes,
            'current_class': current_class,
            'current_class_id_list': [current_class.id] if current_class else [], # <--- Add this line
            'today': today,
        }
        return render(request, 'teacher_dashboard.html', context)
# 3. STUDENT CHECK
    try:
        student_profile = StudentProfile.objects.get(user=user)
        # Fetch their marks and latest attendance to show on their profile
        marks = Mark.objects.filter(student=student_profile).first()
        assignments = Assignment.objects.filter(student=student_profile)
        
        # Calculate overall attendance percentage
        all_attendance = Attendance.objects.filter(student=student_profile)
        total_days = all_attendance.count()
        present_days = all_attendance.filter(status=True).count()
        attendance_percentage = int((present_days / total_days) * 100) if total_days > 0 else 0

        context = {
            'profile': student_profile,
            'marks': marks,
            'assignments': assignments,
            'total_days': total_days,
            'present_days': present_days,
            'attendance_percentage': attendance_percentage
        }
        return render(request, 'student_dashboard.html', context)
    except StudentProfile.DoesNotExist:
        return render(request, 'login.html', {'error': 'Profile not found!'})

def login_user(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def register_student(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == "POST":
        u_name = request.POST.get('username')
        u_pass = request.POST.get('password')
        u_roll = request.POST.get('roll_number')
        u_dept = request.POST.get('department')

        # 1. Create the User
        new_user = User.objects.create_user(username=u_name, password=u_pass)
        
        # 2. Create the Profile
        StudentProfile.objects.create(
            user=new_user, 
            roll_number=u_roll, 
            department=u_dept,
            fees_paid=False 
        )
        return redirect('dashboard')
        
    return render(request, 'register_student.html') 

@login_required
def update_student_data(request, student_id):
    # Only Teachers and Admins can update marks
    is_teacher = request.user.groups.filter(name='Teacher').exists() or request.user.username.startswith('teacher')
    if not (is_teacher or request.user.is_superuser):
        return redirect('dashboard')

    student = get_object_or_404(StudentProfile, id=student_id)
    
    # SECURITY: Ensure teacher can only update their own students (unless superuser)
    if not request.user.is_superuser:
        if not StudentClass.objects.filter(teacher=request.user, id=student.assigned_class_id).exists():
            return redirect('dashboard')

    # Get or create the marks/assignment records for this student
    marks, _ = Mark.objects.get_or_create(student=student)
    assignment, _ = Assignment.objects.get_or_create(student=student)

    if request.method == "POST":
        internal = request.POST.get('internal')
        external = request.POST.get('external')
        
        # If nothing is provided, use a static '0' so it's not void
        marks.internal_marks = int(internal) if internal else 0
        marks.external_marks = int(external) if external else 0
        
        assignment.is_submitted = 'is_submitted' in request.POST
        
        marks.save()
        assignment.save()
        return redirect('dashboard')

    return render(request, 'update_marks.html', {
        'student': student,
        'marks': marks,
        'assignment': assignment
    })

@login_required
def mark_attendance(request):
    # Only Teachers and Admins can mark attendance
    is_teacher = request.user.groups.filter(name='Teacher').exists() or request.user.username.startswith('teacher')
    if not (is_teacher or request.user.is_superuser):
        return redirect('dashboard')

    today = date.today()
    
    # Filter students by the Teacher's class
    if request.user.is_superuser:
        students = StudentProfile.objects.all()
    else:
        my_classes = StudentClass.objects.filter(teacher=request.user)
        selected_class_id = request.GET.get('class_id')
        if selected_class_id:
            current_class = get_object_or_404(StudentClass, id=selected_class_id)
            students = StudentProfile.objects.filter(assigned_class=current_class)
        else:
            current_class = my_classes.first()
            students = StudentProfile.objects.filter(assigned_class=current_class) if current_class else StudentProfile.objects.none()

    if request.method == "POST":
        # Get list of student IDs that are checked (meaning they are present)
        present_student_ids = request.POST.getlist('attendance')
        
        for student in students:
            is_present = str(student.id) in present_student_ids
            
            # Use update_or_create so we don't have duplicate records for the same day
            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={'status': is_present}
            )
            
        return redirect('dashboard')

    # Get last 2 days attendance summary
    past_dates = [today - timedelta(days=1), today - timedelta(days=2)]
    recent_attendance = []
    for d in past_dates:
        records = Attendance.objects.filter(student__in=students, date=d)
        if records.exists():
            present_c = records.filter(status=True).count()
            absent_c = records.filter(status=False).count()
            recent_attendance.append({
                'date': d,
                'present': present_c,
                'absent': absent_c,
                'total': present_c + absent_c
            })

    context = {
        'students': students,
        'today': today,
        'recent_attendance': recent_attendance,
        'my_classes': my_classes if not request.user.is_superuser else None,
        'current_class': current_class if not request.user.is_superuser else None
    }
    return render(request, 'mark_attendance.html', context)
