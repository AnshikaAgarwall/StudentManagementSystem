from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-student/', views.register_student, name='register_student'),
    path('logout/', views.logout_user, name='logout'),
    path('update-student/<int:student_id>/', views.update_student_data, name='update_student'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
]