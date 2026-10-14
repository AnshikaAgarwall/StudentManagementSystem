# 🔑 Student Management System - Login Credentials & Quick Guide

Ye file aapke reference ke liye hai taaki agar aap credentials ya commands bhool jayein, to yahan se dekh sakein.

---

## ⚡ Virtual Environment & Run Commands

### 1. Virtual Environment Activate Kaise Karein:
- **PowerShell (VS Code Terminal):**
  ```powershell
  E:\sms_env\Scripts\Activate.ps1
  ```
  *(Agar execution policy block kare to pehle run karein: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

- **Command Prompt (CMD):**
  ```cmd
  E:\sms_env\Scripts\activate.bat
  ```

### 2. Server Start Karne Ke Liye:
```powershell
# Agar venv activated hai:
python manage.py runserver

# Ya direct bina activate kiye (100% Guaranteed):
E:\sms_env\Scripts\python.exe manage.py runserver
```
👉 Browser URL: **http://127.0.0.1:8000/**

---

## 👥 Realistic Multi-Class Login Credentials

> **Common Password:** Sabhi accounts ka default password **`password123`** hai.

### 1. 👑 Admin Accounts (Superuser)
Full access (All students, unassigned students, registration & admin panel):
| Username | Password | Role | Features |
| :--- | :--- | :--- | :--- |
| **`admin_user1`** | `password123` | Superuser | Master student database, add new students, manage faculty |
| **`admin_user2`** | `password123` | Superuser | Full system administration |

Django Admin Panel URL: **http://127.0.0.1:8000/admin/**

---

### 2. 👨‍🏫 Faculty / Teacher Accounts (Multiple Classes per Teacher)
Har teacher ke paas real-world university pattern me **multiple classes & sections** hain. Login karne par dropdown se easily switch kar sakte hain:

| Faculty Username | Password | Assigned Classes & Sections | Total Classes |
| :--- | :--- | :--- | :---: |
| **`teacher1`** *(Senior Faculty - CS)* | `password123` | • **MCA (Section A)**<br>• **MCA (Section B)**<br>• **B.Tech CSE (Section A)** | **3 Classes** |
| **`teacher2`** *(Management Faculty)* | `password123` | • **MBA (Section A)**<br>• **MBA (Section B)**<br>• **BBA (Section A)** | **3 Classes** |
| **`teacher3`** *(Engineering Faculty)* | `password123` | • **B.Tech CSE (Section B)**<br>• **B.Tech IT (Section A)** | **2 Classes** |
| **`teacher4`** *(Applied Science)* | `password123` | • **BCA (Section A)**<br>• **MCA (Section C)** | **2 Classes** |

---

### 3. 🎓 Student Accounts (Realistic Diverse Profiles)
Apne personal marks, assignment status, aur attendance percentage dekhna:

| Username | Password | Dept | Class & Section | Fees Status | Academic Standing |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`anshika`** | `password123` | MCA | MCA Section A | Paid | Excellent (92%) |
| **`rahul`** | `password123` | MCA | MCA Section A | Paid | Average (78%) |
| **`sneha`** | `password123` | MCA | MCA Section A | **Unpaid** | Good Standing |
| **`karan`** | `password123` | MCA | MCA Section A | **Unpaid** | Defaulter (45%) |
| **`vikram`** | `password123` | MCA | MCA Section B | Paid | High Marks |
| **`shivam`** | `password123` | MCA | MCA Section B | **Unpaid** | Average Marks |
| **`pooja`** | `password123` | MCA | MCA Section B | Paid | 100% Attendance |
| **`aditya`** | `password123` | B.Tech | B.Tech CSE Sec A | Paid | Distinction (29/30) |
| **`tanvi`** | `password123` | B.Tech | B.Tech CSE Sec A | Paid | Assignment Pending |
| **`harsh`** | `password123` | B.Tech | B.Tech CSE Sec A | **Unpaid** | Needs Improvement |
| **`kavya`** | `password123` | MBA | MBA Section A | Paid | Top Performer |
| **`rohan`** | `password123` | MBA | MBA Section A | **Unpaid** | Cleared Submissions |
| **`aman`** | `password123` | MBA | MBA Section A | Paid | Regular |
| **`neha`** | `password123` | MBA | MBA Section B | Paid | High Scorer |
| **`priya`** | `password123` | MBA | MBA Section B | Paid | Average |
| **`arjun`** | `password123` | MBA | MBA Section B | **Unpaid** | Defaulter |
| **`simran`** | `password123` | BBA | BBA Section A | Paid | Active Student |
| **`mohit`** | `password123` | B.Tech | B.Tech CSE Sec B | Paid | Good Standing |
| **`ishaan`** | `password123` | B.Tech | B.Tech IT Sec A | Paid | Top Scorer |
| **`sameer`** | `password123` | BCA | BCA Section A | Paid | Average |
| **`deepak`** | `password123` | MCA | MCA Section C | Paid | Regular |

---

## 🔄 Fresh Data Reset Command
Agar ye realistic multi-class data database me load karna ho to terminal me run karein:
```powershell
python reset_and_seed.py
```
*(Is se 10 classes, 4 teachers jinke paas multiple sections hain, aur 25+ real-looking students 7-day attendance ke sath generate ho jayenge!)*
