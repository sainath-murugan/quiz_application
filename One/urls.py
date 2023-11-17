from django.urls import path
from . import views

urlpatterns = [
    
    path('profile_setup/', views.profileSetup, name="profile_setup"),
    path('educator_dashboard/', views.educatorDashboard, name = 'educator_dashboard'),
    path('create_quiz/', views.create_quiz, name = "create_quiz"),
    path('create_question/',  views.create_question, name="create_question"),
    path('submit_question/', views.submit_question, name="submit_question"),
    path('student_dashboard/', views.studentDashboard, name="student_dashboard"),
    path('attend_quiz/<uuid:id2>/', views.attendQuiz, name='attend_quiz'),
    path('delete_quiz/', views.deleteQuiz, name='delete_quiz'),
   
]