from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard, name="home"),
    path('',views.landing_page, name="landing_page"),
    path('explore',views.explore, name="explore"),
    path('create-project/', views.create_project, name="create_project"),
    path('details-project/<int:pk>', views.project_detail, name="project_detail"),
    path('update-project/<int:pk>', views.update_project, name='update_project'),
    path('student-profile/<int:pk>', views.view_student_profile, name='view_profile'),
    path('teacher-profile/<int:pk>', views.teacher, name='teacher_profile'),
    path('register/', views.student_register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('approvals/', views.pending_approvals, name='pending_approvals'),
    path('approve/<int:student_id>/', views.approve_student, name='approve_student'),
    path('profile-update/', views.update_student_profile, name='update_student_profile'),
    path('team/', views.team, name='team'),
]
