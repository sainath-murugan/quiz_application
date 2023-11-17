from django.shortcuts import redirect

def verify_setResetPassword(func):

    def inner_func(request, *args, **kwargs):
        if request.user.password_reset_choices_verify == False:
            return redirect("account:set_reset_password_question")
        else:
            return func(request, *args, **kwargs)
    return inner_func

def verify_user_authenticated(func):
    
    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.account_type == "STUDENT":
                return redirect("student_dashboard")
            elif request.user.account_type == "EDUCATOR":
                return redirect("educator_dashboard")
        else:
            return func(request, *args, **kwargs)
    return inner_func