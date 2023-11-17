#form displayed in admin page

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationFormAdmin(UserCreationForm): 

    ACCOUNT_TYPE = [
        ("EDUCATOR", "EDUCATOR"),
        ("STUDENT", "STUDENT"),
    ]
        
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE,
        widget=forms.RadioSelect(),
        help_text="select the account type",
    )
    
    class Meta:

        model = CustomUser
        fields = ("__all__") 


class CustomUserChangeFormAdmin(UserChangeForm):
    
    ACCOUNT_TYPE = [
        ("EDUCATOR", "EDUCATOR"),
        ("STUDENT", "STUDENT"),
    ]
        
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE,
        widget=forms.RadioSelect(),
        help_text="select the account type",
    )
    
    class Meta:
        
        model = CustomUser
        fields = ("__all__") 