from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomLoginForm, CustomPasswordChangeForm,\
SetResetPasswordQnForm, ForgotPasswordForm, ResetPasswordForm, ResetPasswordCheckQn, TwoFactor, \
CreateTicket, AnonymousContactForm

from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import verify_setResetPassword, verify_user_authenticated
from django.http import HttpResponseBadRequest
from One.decorators import verify_profile_setup
from .models import Ticket

CustomUser = get_user_model()

@verify_user_authenticated
def signup(request):
    
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user_email = form.cleaned_data.get("email")
                messages.success(request, "you have successfully signed up with the email" + user_email)
                return redirect("account:login")
        else:
            form = CustomUserCreationForm()

        context = {
            "form": form
        }
        return render(request, "account/signup.html", context)

@verify_user_authenticated
def login(request):
   
        if request.method == "POST":
            form = CustomLoginForm(request.POST)
            if form.is_valid():

                user_email = request.POST.get("email")
                user_password = request.POST.get("password")
                next = request.POST.get("next")
                user = authenticate(request, email = user_email, password=user_password)

                if user is not None:
                    auth_login(request, user)
                    messages.info(request, f"you are now logged in {user_email}")

                    if next:
                        return redirect(request.POST.get('next'))
                    else:
                        if request.user.account_type == "STUDENT":
                            return redirect("student_dashboard")
                        elif request.user.account_type == "EDUCATOR":
                            return redirect("educator_dashboard")
                else:
                    messages.error(request, "invalid email or password or user not exist") 
        else:
            form = CustomLoginForm()

        context = {
            "form" : form
        }
        return render(request, "account/login.html", context)

def logout(request):

    auth_logout(request)
    messages.error(request, "you have been logged out") 
    return redirect("account:login")

@login_required(login_url='account:login')
def changePassword(request):

    try:
        CustomUser.objects.get(id=request.user.id)
    except:
       return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.method == "POST":
            form = CustomPasswordChangeForm(request.user, request.POST)                      
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user) # Otherwise the user’s auth session will be invalidated and she/he will have to log in again.
                return redirect("account:profile")
        else:
            form = CustomPasswordChangeForm(request.user)
                
        context = {
            "form" :form
        }
        return render(request, "account/change_password.html", context)
               
@login_required(login_url="account:login")
def setResetPasswordQuestion(request): 

    try:
        CustomUser.objects.get(id=request.user.id)
    except:
       return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:

        if request.user.password_reset_choices_verify == True:
            if request.user.account_type == "STUDENT":
                return redirect("student_dashboard")
            elif request.user.account_type == "EDUCATOR":
                return redirect("educator_dashboard")
            
        else:
            if request.method == "POST":
                form = SetResetPasswordQnForm(request.POST,instance=request.user)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.password_reset_choices_verify = True
                    user.save()
                    if request.user.account_type == "STUDENT":
                        return redirect("student_dashboard")
                    elif request.user.account_type == "EDUCATOR":
                        return redirect("educator_dashboard")  
            else:
                form = SetResetPasswordQnForm(instance=request.user)
                
            context = {
                "form" :form
            }
            return render(request, "account/set_reset_password_question.html", context)
            
@verify_user_authenticated
def forgotPassword(request):
    
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_email = request.POST.get("email")
            user = CustomUser.objects.get(email = user_email)
            return redirect("account:reset_password_check_qn", str(user.id))
    else:
        form = ForgotPasswordForm()

    context = {
        "form" :form
    }
    return render(request, "account/forgot_password.html", context)

@verify_user_authenticated 
def resetPasswordCheckQn(request, id):

    try:
        current_user = CustomUser.objects.get(id=id)
    except:
       return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.method == "POST":
            form = ResetPasswordCheckQn(request.POST, current_user_reset_ans=current_user.password_reset_choices_ans)
            if form.is_valid():   
                return redirect("account:reset_password", current_user.id)
        else:
            form =  ResetPasswordCheckQn()
            
        context = {
            "id" :id,
            "qn": current_user.password_reset_choices_qn,
            "form": form
        }
        return render(request, "account/reset_password_check_qn.html", context)

@verify_user_authenticated
def resetPassword(request, id):

    try:
        current_user = CustomUser.objects.get(id=id)
    except:
       return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password2 = request.POST.get("new_password2")
                current_user.set_password(new_password2)
                current_user.save()
                messages.success(request, "password re-setted successfully")
                return redirect("account:login")
        else:
            form = ResetPasswordForm()

        context = {
                "id" :id,
                "form": form
        }
        return render(request, "account/reset_password.html", context)
    
@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def profilePage(request):

    try:
        CustomUser.objects.get(id=request.user.id)
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else: 
        return render(request, "account/profile.html")
       
@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def twoFactor(request):

    try:
        CustomUser.objects.get(id=request.user)
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.method == "POST":
            form = TwoFactor(request.POST, request=request)
            if form.is_valid():          
                return redirect("account:two_factor")
        else:
            form = TwoFactor(request=request)

        context = {
            'form': form
        }
        return render(request, "account/two_factor.html", context)
             
@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def deleteLoginHistory(request):

    try:
        CustomUser.objects.get(id=request.user.id)
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        if request.method == "POST":     
            request.user.user_history.all().delete()    
            return redirect('account:profile')
        else:
            return redirect("account:profile")
        
@login_required(login_url="account:login")
@verify_setResetPassword 
@verify_profile_setup 
def createTicket(request):

    try:
        CustomUser.objects.get(id=request.user.id)
    except:
        return HttpResponseBadRequest('some error occured, Maybe this user id not exits anymore')
    else:
        try: 
            Ticket.objects.get(user=request.user)
        except:
            if request.method == "POST":
                form = CreateTicket(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.user = request.user
                    form.save()
                    return redirect('account:profile')
            else:
                form = CreateTicket()
            
            context = {
                'form': form
            }
            return render(request, "account/ticket.html", context)
        else:
            return redirect('account:profile')
        

@verify_user_authenticated
def anonymousContact(request):

    if request.method == "POST":
            form = AnonymousContactForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("account:login")
    else:
        form = AnonymousContactForm()

    context = {
            "form": form
    }
    return render(request, "account/anonymous_contact.html", context)