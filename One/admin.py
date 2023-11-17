from django.contrib import admin
from .models import College, UserProfileEducator, Course, UserProfileStudent,\
QuestionForQuiz, Quiz, StudentMark

from .admin_forms import CreateQuestionModelAdmin, UserProfileEducatorFormAdmin, UserProfileStudentFormAdmin,\
QuizFormAdmin

class ModelAdmin(admin.ModelAdmin): #admin validation

    form = CreateQuestionModelAdmin

class ModelAdmin2(admin.ModelAdmin): #admin validation

    form = UserProfileEducatorFormAdmin
    

class ModelAdmin3(admin.ModelAdmin): #admin validation

    form = UserProfileStudentFormAdmin

class ModelAdmin4(admin.ModelAdmin): #admin validation
    
    form = QuizFormAdmin
    
admin.site.register(QuestionForQuiz, ModelAdmin)
admin.site.register(UserProfileEducator, ModelAdmin2)
admin.site.register(UserProfileStudent, ModelAdmin3)
admin.site.register(Quiz, ModelAdmin4)
admin.site.register(StudentMark)
admin.site.register(Course)
admin.site.register(College)