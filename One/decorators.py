from django.shortcuts import redirect

def verify_profile_setup(func):
    
    def inner_func(request, *args, **kwargs):
        
        if request.user.account_type == "EDUCATOR":
            if request.user.user_profile_educator.educator_profile_setup_verify == False:
                return redirect("profile_setup")
            else:
                return func(request, *args, **kwargs)
        elif request.user.account_type == "STUDENT":
            
            if request.user.user_profile_student.student_profile_setup_verify == False:
                return redirect("profile_setup")
            else:
                return func(request, *args, **kwargs)
    return inner_func