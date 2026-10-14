import csv
from datetime import date, timedelta, datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Mark, Assignment, Attendance, StudentClass, ClassAssignment, StudentSubmission


def is_teacher_user(user):
    """Check if user has faculty/teacher privileges via Staff status or Teacher group."""
    return user.is_staff or user.groups.filter(name='Teacher').exists()

@login_required
def dashboard(request):
    user = request.user
    today = date.today()

    # 1. ADMIN CHECK
    if user.is_superuser:
        total_teachers = User.objects.filter(groups__name='Teacher').count()
        if total_teachers == 0:
            total_teachers = User.objects.filter(is_staff=True, is_superuser=False).count()

        context = {
            'total_students': StudentProfile.objects.count(),
            'unpaid_fees': StudentProfile.objects.filter(fees_paid=False).count(),
            'total_teachers': total_teachers,
            'students': StudentProfile.objects.select_related('user', 'assigned_class').all(),
        }
        return render(request, 'admin_dashboard.html', context)

    # 2. TEACHER CHECK
    if is_teacher_user(user):
        my_classes = StudentClass.objects.filter(teacher=user)
        selected_class_id = request.GET.get('class_id')

        if selected_class_id:
            current_class = my_classes.filter(id=selected_class_id).first() or StudentClass.objects.filter(id=selected_class_id).first()
        else:
            current_class = my_classes.first()

        if current_class:
            students = StudentProfile.objects.filter(assigned_class=current_class).select_related('user').prefetch_related('attendance_set', 'assignment_set', 'mark_set')
            today_records = Attendance.objects.filter(student__in=students, date=today)
            today_taken = today_records.exists()
            today_present_count = today_records.filter(status=True).count()
        else:
            students = StudentProfile.objects.none()
            today_taken = False
            today_present_count = 0

        context = {
            'students': students,
            'my_classes': my_classes,
            'current_class': current_class,
            'current_class_id_list': [current_class.id] if current_class else [],
            'today': today,
            'today_taken': today_taken,
            'today_present_count': today_present_count,
        }
        return render(request, 'teacher_dashboard.html', context)

    # 3. STUDENT CHECK
    try:
        student_profile = StudentProfile.objects.select_related('user', 'assigned_class').get(user=user)
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

    classes = StudentClass.objects.all()

    if request.method == "POST":
        u_name = request.POST.get('username', '').strip()
        u_pass = request.POST.get('password', '').strip()
        u_roll = request.POST.get('roll_number', '').strip()
        u_dept = request.POST.get('department', '').strip()
        class_id = request.POST.get('assigned_class')

        if User.objects.filter(username=u_name).exists():
            return render(request, 'register_student.html', {
                'classes': classes,
                'error': f"User '{u_name}' already exists! Choose a different username."
            })

        assigned_class = StudentClass.objects.filter(id=class_id).first() if class_id else None

        # 1. Create the User
        new_user = User.objects.create_user(username=u_name, password=u_pass)

        # 2. Create the Profile
        new_profile = StudentProfile.objects.create(
            user=new_user,
            roll_number=u_roll,
            department=u_dept,
            fees_paid=False,
            assigned_class=assigned_class
        )

        # 3. Create initial Marks & Assignment
        Mark.objects.create(student=new_profile, internal_marks=0, external_marks=0)
        Assignment.objects.create(student=new_profile, is_submitted=False)

        return redirect('dashboard')

    return render(request, 'register_student.html', {'classes': classes})

@login_required
def update_student_data(request, student_id):
    if not (is_teacher_user(request.user) or request.user.is_superuser):
        return redirect('dashboard')

    student = get_object_or_404(StudentProfile, id=student_id)

    # Security: Ensure teacher can only update students from their assigned classes
    if not request.user.is_superuser:
        if not StudentClass.objects.filter(teacher=request.user, id=student.assigned_class_id).exists():
            return redirect('dashboard')

    marks, _ = Mark.objects.get_or_create(student=student)
    assignment, _ = Assignment.objects.get_or_create(student=student)

    if request.method == "POST":
        internal_raw = request.POST.get('internal', '').strip()
        external_raw = request.POST.get('external', '').strip()

        try:
            internal_val = int(internal_raw) if internal_raw else 0
            external_val = int(external_raw) if external_raw else 0
        except ValueError:
            internal_val = 0
            external_val = 0

        # Boundary checks: Internal (max 30), External (max 70)
        marks.internal_marks = max(0, min(30, internal_val))
        marks.external_marks = max(0, min(70, external_val))
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
    if not (is_teacher_user(request.user) or request.user.is_superuser):
        return redirect('dashboard')

    today = date.today()

    # Determine date (today or custom selected date)
    date_str = request.POST.get('attendance_date') or request.GET.get('attendance_date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = today
    else:
        target_date = today

    if request.user.is_superuser:
        available_classes = StudentClass.objects.all()
    else:
        available_classes = StudentClass.objects.filter(teacher=request.user)

    # Get selected class from POST (priority) or GET
    selected_class_id = request.POST.get('class_id') or request.GET.get('class_id')
    current_class = None

    if selected_class_id:
        current_class = available_classes.filter(id=selected_class_id).first()

    if not current_class and available_classes.exists():
        current_class = available_classes.first()

    if current_class:
        students = list(StudentProfile.objects.filter(assigned_class=current_class).select_related('user'))
    elif request.user.is_superuser:
        students = list(StudentProfile.objects.all().select_related('user'))
    else:
        students = []

    # Check existing attendance for this specific date
    existing_records = Attendance.objects.filter(student__in=students, date=target_date)
    attendance_already_taken = existing_records.exists()
    present_student_ids = set(existing_records.filter(status=True).values_list('student_id', flat=True))

    # Pre-populate each student object with current status on this date
    for s in students:
        s.is_marked_present = (s.id in present_student_ids)

    if request.method == "POST":
        submitted_present_ids = request.POST.getlist('attendance')

        for student in students:
            is_present = str(student.id) in submitted_present_ids
            Attendance.objects.update_or_create(
                student=student,
                date=target_date,
                defaults={'status': is_present}
            )

        redirect_query = f"?class_id={current_class.id}&attendance_date={target_date.strftime('%Y-%m-%d')}&saved=1" if current_class else f"?attendance_date={target_date.strftime('%Y-%m-%d')}&saved=1"
        return redirect(f"{request.path}{redirect_query}")

    # Get last 2 days attendance summary (excluding target_date if desired)
    past_dates = [target_date - timedelta(days=1), target_date - timedelta(days=2)]
    recent_attendance = []
    if students:
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
        'target_date': target_date,
        'attendance_already_taken': attendance_already_taken,
        'present_count': len(present_student_ids),
        'recent_attendance': recent_attendance,
        'my_classes': available_classes,
        'current_class': current_class,
        'is_saved': request.GET.get('saved') == '1'
    }
    return render(request, 'mark_attendance.html', context)

@login_required
def export_attendance_csv(request):
    if not (is_teacher_user(request.user) or request.user.is_superuser):
        return redirect('dashboard')

    today = date.today()
    class_id = request.GET.get('class_id')
    month_str = request.GET.get('month') # Format: YYYY-MM

    if month_str:
        try:
            year, month = map(int, month_str.split('-'))
        except ValueError:
            year, month = today.year, today.month
    else:
        year, month = today.year, today.month

    # Filter classes
    if request.user.is_superuser:
        available_classes = StudentClass.objects.all()
    else:
        available_classes = StudentClass.objects.filter(teacher=request.user)

    target_class = available_classes.filter(id=class_id).first() if class_id else available_classes.first()

    if target_class:
        students = list(StudentProfile.objects.filter(assigned_class=target_class).select_related('user'))
        class_name_str = f"{target_class.class_name}_Sec_{target_class.section}"
    elif request.user.is_superuser:
        students = list(StudentProfile.objects.all().select_related('user'))
        class_name_str = "All_Classes"
    else:
        students = []
        class_name_str = "No_Class"

    # Distinct dates on which attendance was recorded in this month
    recorded_dates = list(Attendance.objects.filter(
        student__in=students,
        date__year=year,
        date__month=month
    ).values_list('date', flat=True).distinct().order_by('date'))

    filename = f"Attendance_{class_name_str}_{year}_{month:02d}.csv"
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # Header section
    month_name = datetime(year, month, 1).strftime('%B %Y')
    writer.writerow([f"MONTHLY ATTENDANCE REGISTER - {month_name.upper()}"])
    writer.writerow([f"Class/Section: {target_class if target_class else 'All'}", f"Exported By: {request.user.username}", f"Date: {today.strftime('%d-%b-%Y')}"])
    writer.writerow([])

    # Table columns: Info + Daily Columns (P/A) + Totals + Status
    header_row = ['Roll Number', 'Student Name', 'Department']
    for d in recorded_dates:
        header_row.append(d.strftime('%d-%b'))
    header_row.extend(['Total Days', 'Present Days', 'Absent Days', 'Attendance %', 'Eligibility (>=75%)'])
    writer.writerow(header_row)

    # Populate rows for each student
    for s in students:
        # Map date -> status for this student
        student_records = {
            att.date: att.status for att in Attendance.objects.filter(
                student=s,
                date__year=year,
                date__month=month
            )
        }

        total_days = len(recorded_dates)
        present_days = sum(1 for d in recorded_dates if student_records.get(d) is True)
        absent_days = sum(1 for d in recorded_dates if student_records.get(d) is False)
        
        pct = round((present_days / total_days) * 100, 1) if total_days > 0 else 0.0
        eligibility = "ELIGIBLE" if pct >= 75 else ("DEFAULTER" if total_days > 0 else "NO DATA")

        row = [s.roll_number, s.user.username.title(), s.department]
        for d in recorded_dates:
            st = student_records.get(d)
            if st is True:
                row.append('P')
            elif st is False:
                row.append('A')
            else:
                row.append('-')

        row.extend([total_days, present_days, absent_days, f"{pct}%", eligibility])
        writer.writerow(row)

    return response

@login_required
def manage_assignments(request):
    if not (is_teacher_user(request.user) or request.user.is_superuser):
        return redirect('dashboard')

    if request.user.is_superuser:
        my_classes = StudentClass.objects.all()
        assignments = ClassAssignment.objects.all().order_by('-created_at')
    else:
        my_classes = StudentClass.objects.filter(teacher=request.user)
        assignments = ClassAssignment.objects.filter(teacher=request.user).order_by('-created_at')

    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        class_id = request.POST.get('assigned_class')
        due_date_str = request.POST.get('due_date')
        ref_file = request.FILES.get('reference_file')

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                due_date = None

        target_class = my_classes.filter(id=class_id).first()
        if title and target_class:
            ClassAssignment.objects.create(
                title=title,
                description=description,
                assigned_class=target_class,
                teacher=request.user,
                due_date=due_date,
                reference_file=ref_file
            )
            return redirect('manage_assignments')

    return render(request, 'manage_assignments.html', {
        'my_classes': my_classes,
        'assignments': assignments
    })

@login_required
def view_submissions(request, assignment_id):
    if not (is_teacher_user(request.user) or request.user.is_superuser):
        return redirect('dashboard')

    assignment = get_object_or_404(ClassAssignment, id=assignment_id)

    # Security check: Teacher must own assignment or be superuser
    if not request.user.is_superuser and assignment.teacher != request.user:
        return redirect('dashboard')

    students = StudentProfile.objects.filter(assigned_class=assignment.assigned_class).select_related('user')
    submissions = {sub.student_id: sub for sub in StudentSubmission.objects.filter(assignment=assignment)}

    roster = []
    for s in students:
        sub = submissions.get(s.id)
        roster.append({
            'student': s,
            'is_submitted': sub is not None,
            'submission': sub
        })

    return render(request, 'view_submissions.html', {
        'assignment': assignment,
        'roster': roster,
        'total_enrolled': students.count(),
        'total_submitted': len(submissions)
    })

@login_required
def student_assignments(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('dashboard')

    if not profile.assigned_class:
        return render(request, 'student_assignments.html', {
            'profile': profile,
            'assignments_with_status': []
        })

    class_assignments = ClassAssignment.objects.filter(assigned_class=profile.assigned_class).order_by('-created_at')
    submissions = {sub.assignment_id: sub for sub in StudentSubmission.objects.filter(student=profile)}

    if request.method == "POST":
        assignment_id = request.POST.get('assignment_id')
        upload = request.FILES.get('submission_file')
        notes = request.POST.get('notes', '').strip()

        target_assignment = class_assignments.filter(id=assignment_id).first()
        if target_assignment and upload:
            StudentSubmission.objects.update_or_create(
                assignment=target_assignment,
                student=profile,
                defaults={
                    'submission_file': upload,
                    'notes': notes
                }
            )
            # Sync legacy assignment flag
            Assignment.objects.filter(student=profile).update(is_submitted=True)
            return redirect('student_assignments')

    assignments_with_status = []
    for a in class_assignments:
        sub = submissions.get(a.id)
        assignments_with_status.append({
            'assignment': a,
            'is_submitted': sub is not None,
            'submission': sub
        })

    return render(request, 'student_assignments.html', {
        'profile': profile,
        'assignments_with_status': assignments_with_status
    })


