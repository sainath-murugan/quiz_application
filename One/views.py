from django.shortcuts import render, redirect
from user.decorators import verify_setResetPassword
from .decorators import verify_profile_setup
from .models import Quiz, QuestionForQuiz, UserProfileEducator, StudentMark
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .forms import UserProfileEducatorForm, UserProfileStudentForm, QuizFormTitle, CreateQuestion, \
QuizFormPublish

from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# not a router
def check(request):

    if request.user.account_type == "STUDENT":
        if request.user.user_profile_student.student_profile_setup_verify == False:
            return True
        else:
            return False

    elif request.user.account_type == "EDUCATOR":
        if request.user.user_profile_educator.educator_profile_setup_verify == False:
            return True
        else:
            return False

@login_required(login_url="account:login")
def profileSetup(request):

    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        res = check(request)
        if res == True:
            if request.method == "POST":
                if request.user.account_type == "STUDENT":
                    form = UserProfileStudentForm(request.POST, instance=request.user.user_profile_student)
                    if form.is_valid():
                        profile_verify = form.save(commit=False)
                        profile_verify.student_profile_setup_verify = True
                        profile_verify.save()
                        return redirect("student_dashboard")     
                                
                elif request.user.account_type == "EDUCATOR":
                    form = UserProfileEducatorForm(request.POST, instance=request.user.user_profile_educator)
                    if form.is_valid():
                        profile_verify = form.save(commit=False)
                        profile_verify.educator_profile_setup_verify = True
                        profile_verify.save()
                        return redirect("educator_dashboard")
            else:
                if request.user.account_type == "STUDENT":
                    form = UserProfileStudentForm(instance=request.user.user_profile_student)
                elif request.user.account_type == "EDUCATOR":
                    form = UserProfileEducatorForm(instance=request.user.user_profile_educator)

            context = {
                "form": form
            }
            return render(request, "profile_setup.html", context)
               
        elif res == False:          
            if request.user.account_type == "STUDENT":
                return redirect("student_dashboard")
            elif request.user.account_type == "EDUCATOR":
                return redirect("educator_dashboard")
        
@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def educatorDashboard(request):

    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'EDUCATOR':
            try:
                quiz = Quiz.objects.get(created_by=request.user.user_profile_educator) 
                student_mark = StudentMark.objects.all().filter(quiz=quiz)
            except:
                form = None #unbound error
                student_mark = None
            else: #if no error
                if request.method == "POST": 
                    form = QuizFormPublish(request.POST, instance=request.user.user_profile_educator.created_by_educator)
                    if form.is_valid():
                        form_n = form.save(commit=False) 
                        form_n.publish_verify = True
                        form_n.save()
                        form.save_m2m()
                        return redirect("educator_dashboard")   
                else:
                    form = QuizFormPublish(instance=request.user.user_profile_educator.created_by_educator)
                          
            context = {
                'form': form,
                'student_mark': student_mark    
            }
            return render(request, "educator_dashboard.html", context)
        
        elif request.user.account_type == 'STUDENT':
                return redirect("student_dashboard")


@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def create_quiz(request):

    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'EDUCATOR':
            try:
                Quiz.objects.get(created_by=request.user.user_profile_educator)
            except:
                if request.method == "POST":
                    form = QuizFormTitle(request.POST)
                    if form.is_valid():    
                        form = form.save(commit=False)  
                        form.created_by = request.user.user_profile_educator
                        form.save()
                        return redirect("create_question")
                   
                else:
                    form = QuizFormTitle() 
                       
                context = {
                    "form": form
                    }
                return render(request, "create_quiz.html", context)
                
            else: #if no error
                return redirect("educator_dashboard")
            
        elif request.user.account_type == 'STUDENT':
                return redirect("student_dashboard")

@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def create_question(request):

    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'EDUCATOR':
            try:
                quiz = Quiz.objects.get(created_by=request.user.user_profile_educator) 
            except:
                return HttpResponseBadRequest('some error occured, Maybe this quiz not exits anymore')
            else: #if no error
                if quiz.submitted_verify == True:         
                    return redirect("educator_dashboard")
                else:
                    if request.method == "POST":                              
                        form = CreateQuestion(request.POST)
                        if form.is_valid():
                            form = form.save(commit=False)
                            form.quiz = quiz 
                            form.save()
                            return redirect("create_question")                       
                    else:   
                        form = CreateQuestion()

                    context = {
                        "form": form,
                    }
                    return render(request, "create_question.html", context)
                
        elif request.user.account_type == 'STUDENT':
                return redirect("student_dashboard")

@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def submit_question(request):

    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'EDUCATOR':
            if request.method == "POST":   
                try:     
                    quiz = Quiz.objects.get(created_by=request.user.user_profile_educator)   
                except: 
                    return HttpResponseBadRequest("You have not created quiz to submit")   
                else:                    
                    quiz.submitted_verify = True
                    quiz.save()
                    return redirect("educator_dashboard")
            else:
                return redirect("educator_dashboard")
                    
        elif request.user.account_type == 'STUDENT':
                return redirect("student_dashboard")

@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def studentDashboard(request):
    
    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'STUDENT':
   
            context = {
                'users':  UserProfileEducator.objects.all().filter(college_name=request.user.user_profile_student.college_name)       
            }
               
            return render(request, "student_dashboard.html", context)
            
        elif request.user.account_type == 'EDUCATOR':
            return redirect("educator_dashboard")
        

@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def attendQuiz(request, id2):
    
    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
            return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'STUDENT':
            try:
                quiz = Quiz.objects.get(id=id2)
            except:
                return HttpResponseBadRequest('some error occured, Maybe this quiz not exits anymore')
            else:

                if request.user.user_profile_student.student_quiz_mark.all().filter(quiz=quiz):  
                    return redirect('student_dashboard')
                
                else: 

                    question = QuestionForQuiz.objects.all().filter(quiz=quiz)
                    
                    if request.method == "POST":

                        answer1 = {}
                        for ques in question:
                            if ques.correct_ans == 1:
                                answer1[str(ques)] = ques.choice_one
                            elif ques.correct_ans == 2:
                                answer1[str(ques)] = ques.choice_two
                            elif ques.correct_ans == 3:
                                answer1[str(ques)] = ques.choice_three
                            else:
                                answer1[str(ques)] = ques.choice_four

                        answer2 = {}  
                        for key, value in request.POST.items():
                            if key.startswith('question_'):
                                question_id = key.split('_')[1]
                                answer2[question_id] = value
                        
                        count = 0
                        for ans in answer1:
                            if answer1[ans] == answer2[ans]:
                                count += 1
                 
                        obj = StudentMark.objects.create(
                            student=request.user.user_profile_student,
                            quiz = quiz, 
                            mark = count
                        )
                        obj.save()
                        quiz.students_submitted.add(request.user.user_profile_student)
                        quiz.save()
                        return redirect('student_dashboard')
                   
                    context = {
                        'question': question,
                        'id2': id2,       
                    }
                    return render(request, "attend_quiz.html", context)
                
        elif request.user.account_type == 'EDUCATOR':
                return redirect("educator_dashboard")

@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def deleteQuiz(request):

    try:
        CustomUser.objects.get(id=request.user.id) 
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.user.account_type == 'EDUCATOR':
            if request.method == "POST":
                try:
                    quiz = Quiz.objects.get(created_by=request.user.user_profile_educator) 
                except:
                    return HttpResponseBadRequest('some error occured, Maybe this quiz not exits anymore')
                else:              
                    quiz.delete()
                    return redirect("educator_dashboard")
            else:
                return redirect("educator_dashboard")
            
        elif request.user.account_type == 'STUDENT':
                return redirect("student_dashboard")