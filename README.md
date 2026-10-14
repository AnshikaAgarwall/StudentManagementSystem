# 🎓 EduManage - University & Student Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-003B57.svg?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-stack, enterprise-grade academic management web application built with **Python & Django**. Designed for colleges and universities to manage multi-department academic records, daily attendance tracking, coursework submissions, fee reconciliation, and automated analytics.

---

## ✨ Key Feature Highlights

### 1. 👨‍🏫 Faculty & Teacher Control
- **Multi-Class Section Switching:** Faculty can teach across multiple departments (e.g. *MCA Sec A*, *MCA Sec B*, *B.Tech CSE Sec A*) and toggle between them instantly with an intuitive dropdown.
- **Dynamic Attendance Hub:** Record attendance daily. If taken earlier, previously marked students are **pre-checked automatically**, allowing hassle-free in-place updates for late arrivals without overwriting prior records.
- **1-Click Monthly Excel/CSV Export:** Exports formatted monthly sheets complete with daily `P`/`A` records, total working days, attendance percentage, and automated **75% university rule compliance** (`ELIGIBLE` vs `DEFAULTER`).
- **Assignment Publishing:** Create coursework assignments for specific classes with due dates, formatting guidelines, and optional syllabus/question paper attachments.
- **Document Review & Download:** View student submissions, verify submission timestamps, and download uploaded student papers (`.pdf`, `.docx`, `.doc`).

### 2. 🎓 Student Academic Portal
- **Performance Overview:** Real-time metrics for Attendance Percentage (with visual progress bar), Tuition Fee status, and Total GPA.
- **Grade Breakdown:** Transparent tracking of Internal Assessment marks (/30) and External Semester Exam scores (/70).
- **Online Coursework Submission:** Direct document upload interface for class assignments with support for `.pdf` and Word documents.

### 3. 👑 Administrator Overview
- **Master Student Directory:** University-wide view of all enrolled students, assigned sections, and tuition status.
- **Student Enrollment:** Register new student accounts with automatic user profile creation and class section mapping.
- **Django Admin Integration:** Full CRUD capabilities with model auditing and permission groups.

---

## 🏛️ Architecture & Database Schema

```
                  ┌──────────────────────┐
                  │      Django User     │
                  └──────────┬───────────┘
                             │ (1:1 / 1:N)
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐   ┌───────▼────────┐   ┌───────▼────────┐
│ StudentProfile │   │  StudentClass  │   │     Group      │
└───────┬────────┘   └───────┬────────┘   │  ('Teacher')   │
        │                    │            └────────────────┘
        ├────────────────────┤
        │                    │
┌───────▼────────┐   ┌───────▼────────┐   ┌────────────────┐
│   Attendance   │   │ClassAssignment │◄──┤StudentSubmiss..│
│(Unique Per Day)│   │  (Due Dates)   │   │  (PDF / Word)  │
└────────────────┘   └────────────────┘   └────────────────┘
```

---

## 📁 Project Structure

```
StudentManagement/
├── StudentManagement/          # Project configuration
│   ├── settings.py             # Environment-ready settings & media config
│   ├── urls.py                 # Core URL routing & media serving
│   ├── wsgi.py                 # WSGI application entrypoint
│   └── asgi.py                 # ASGI configuration
├── students/                   # Main application
│   ├── models.py               # Database schemas with relations
│   ├── views.py                # Business logic & controller endpoints
│   ├── urls.py                 # Application sub-routes
│   ├── forms.py                # Django ModelForms for validation
│   ├── admin.py                # Django admin registrations
│   ├── tests.py                # Unit test suite
│   └── templates/              # Modern UI templates (Plus Jakarta Sans)
│       ├── base.html           # Unified responsive layout & dark sidebar
│       ├── login.html          # Glassmorphic authentication portal
│       ├── teacher_dashboard.html # Faculty controls & grade overview
│       ├── student_dashboard.html # Student progress & exam breakdown
│       ├── admin_dashboard.html   # Master institution metrics
│       ├── mark_attendance.html   # Editable attendance hub
│       ├── manage_assignments.html# Coursework publishing & review
│       ├── view_submissions.html  # Student document download hub
│       ├── student_assignments.html # Student file submission portal
│       └── register_student.html  # Enrollment interface
├── media/                      # Uploaded assignments & question papers
├── reset_and_seed.py           # Standalone automated database seeder
├── requirements.txt            # Production dependencies
├── CREDENTIALS.md              # Demo login credentials reference
└── manage.py                   # Django CLI management script
```

---

## 🚀 Getting Started & Local Setup

### Prerequisites
- Python 3.10+ installed
- Git

### 1. Clone & Set Up Virtual Environment
```bash
# Clone the repository
git clone https://github.com/AnshikaAgarwall/StudentManagementSystem.git
cd StudentManagementSystem/StudentManagement

# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```bash
python reset_and_seed.py
```
*This command runs migrations and seeds 10 realistic class sections, 4 faculty accounts, 25+ students across MCA, MBA, and B.Tech, 7-day attendance logs, and sample assignments.*

### 4. Start Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 🧪 Running Unit Tests

The test suite covers user profile creation, daily attendance uniqueness, grade summation, and class assignments:

```bash
python manage.py test
```

Expected output:
```
Found 5 test(s).
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 5 tests in 0.85s

OK
```

---

## 👥 Demo Login Credentials

> All accounts share the common password: **`password123`**

| Role | Username | Password | Assigned Scope |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin_user1` | `password123` | Full System Administration |
| **Faculty** | `teacher1` | `password123` | MCA Sec A, MCA Sec B, B.Tech CSE Sec A |
| **Faculty** | `teacher2` | `password123` | MBA Sec A, MBA Sec B, BBA Sec A |
| **Student** | `anshika` | `password123` | MCA Section A (92% Attendance) |
| **Student** | `aditya` | `password123` | B.Tech CSE Section A (Distinction) |
| **Student** | `karan` | `password123` | MCA Section A (Defaulter Demo) |

*(Full roster documented in [`CREDENTIALS.md`](CREDENTIALS.md))*

---

## 🛡️ Security & Best Practices
- **Role-Based Access Control (RBAC):** Strictly enforced using Django's permission groups and `is_staff` flags.
- **CSRF Protection:** Enabled on all form submissions and API endpoints.
- **Environment Fallbacks:** `SECRET_KEY` and `DEBUG` safely configured with fallback defaults for local development and environment variables for deployment.
- **Strict Query Scoping:** Faculty queries strictly filtered by `assigned_class.teacher = request.user` to prevent unauthorized cross-class tampering.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
