from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from .models import CustomUser, Ticket, AnonymousContact
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
import pyotp

class CustomUserCreationForm(UserCreationForm): 

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        ),
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your password'
            }
        ),
        help_text="""<p>Your password can’t be too similar to your other personal information.</p>
                    <p>Your password must contain at least 8 characters.</p>
                    <p>Your password can’t be a commonly used password.</p>
                    <p>Your password can’t be entirely numeric.</p>"""
    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': 'Enter your password again'
            }
        ),
    )

    ACCOUNT_TYPE = [
        ("EDUCATOR", "EDUCATOR"),
        ("STUDENT", "STUDENT"),
    ]
        
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE,
        widget=forms.RadioSelect(),
        help_text="select the account type",
        label=''
    )
    
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2", 'account_type') 

class CustomUserChangeForm(UserChangeForm): #not used
    
    class Meta:

        model = CustomUser
        fields = ("email",) 
    
class CustomLoginForm(forms.Form): #forms.Form is used instead of inbuilt login form because django uses username as unique id, very complicated to alter in backend.py file
    
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        ),
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }
        ),
    )

    secret_code = forms.CharField(
        max_length=6,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your six digit code if enabled'
            }
        ),
        required=False
    )

    def clean(self):

        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        secret_code = cleaned_data.get('secret_code')
        
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password. Please try again.")
        else:
            if user.authenticator_enable == True:
                if secret_code:
                    totp = pyotp.TOTP(user.authenticator.authenticator_secret_code)
                    if totp.verify(secret_code):
                        return cleaned_data
                    else:
                        raise forms.ValidationError("wrong secret code, enter correctly")
                else:
                        raise forms.ValidationError("you have enabled Two Factor Authentication, enter your secret code")
            else:
                return cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your old password'
            }
        ),
    )

    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Enter your new password'
                }
            ),
        help_text="""<p>Your password can’t be too similar to your other personal information.</p>
                    <p>Your password must contain at least 8 characters.</p>
                    <p>Your password can’t be a commonly used password.</p>
                    <p>Your password can’t be entirely numeric.</p>"""
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your new password again'
            }
        ),
    )

class SetResetPasswordQnForm(forms.ModelForm):

    CHOICE_FOR_RESET_PASSWORD = [
        ("YOUR LUCKEY NUMBER", "YOUR LUCKEY NUMBER"), 
        ("YOUR BEST FRIEND NAME", "YOUR BEST FRIEND NAME"),
        ("YOUR FAVOURITE FOOD", "YOUR FAVOURITE FOOD"),
        ("YOUR FAVOURITE DESTINATION", "YOUR FAVOURITE DESTINATION")
    ]

    password_reset_choices_qn = forms.ChoiceField(
        label='',
        choices=CHOICE_FOR_RESET_PASSWORD,
    )
    
    password_reset_choices_ans = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your answer'
            }
        ),
    )

    class Meta:

        model = CustomUser
        fields = ('password_reset_choices_qn','password_reset_choices_ans')

    def clean_password_reset_choices_ans(self):

        password_reset_choices_ans = self.cleaned_data['password_reset_choices_ans']
        return str(password_reset_choices_ans)

class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Enter your email'
            }
        ),
    )

    def clean_email(self):

        user_email = self.cleaned_data['email']

        try:
            user = CustomUser.objects.get(email = user_email)     
        except:
            raise forms.ValidationError("No user exists with this email") 
        else:
            if user.password_reset_choices_ans:
                return user_email
            else:
                raise forms.ValidationError("you have not set your secret question during account creation, you can't reset your password. please contact the admin")
            
        
class ResetPasswordForm(forms.Form):

    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your password'
            }
        ),
        help_text="""<p>Your password can’t be too similar to your other personal information.</p>
                    <p>Your password must contain at least 8 characters.</p>
                    <p>Your password can’t be a commonly used password.</p>
                    <p>Your password can’t be entirely numeric.</p>""",
        validators=[validate_password]
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your password again'}
        ),
        validators=[validate_password]
    )

    def clean(self):
        
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("enter the same password as above")
        else:
            return new_password2
            
class ResetPasswordCheckQn(forms.Form):

    ans = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your answer'
            }
        ),
    )

    def __init__(self, *args, **kwargs):

        self.current_user_reset_ans = kwargs.pop("current_user_reset_ans", None)
        super().__init__(*args, **kwargs)

    def clean_ans(self):
        
        ans = self.cleaned_data['ans']
        if ans == str(self.current_user_reset_ans):
            return ans
        else:
            raise forms.ValidationError("This is not the correct answer for your reset question")
        
class TwoFactor(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    secret_code = forms.CharField(
        max_length=6,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your six digit code'
            }
        ),
    )

    def clean_secret_code(self):

        secret_code = self.cleaned_data['secret_code']
        totp = pyotp.TOTP(self.request.user.authenticator.authenticator_secret_code)
        if totp.verify(secret_code):

            if self.request.user.authenticator_enable == False:
                self.request.user.authenticator_enable = True
                self.request.user.save()

            elif self.request.user.authenticator_enable == True:
                self.request.user.authenticator_enable = False
                self.request.user.save()
        else:
            raise forms.ValidationError("The six digit secret code you entered is not correct")
        
class CreateTicket(forms.ModelForm):

    title = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your title'
            }
        ),
    )

    message = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your query or message',
            }
        )
    )

    class Meta:

        model = Ticket
        fields = ('title','message')

class AnonymousContactForm(forms.ModelForm):

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        ),
    )

    title = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your title'
            }
        ),
    )

    message = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your query or message',
            }
        )
    )

    class Meta:

        model = AnonymousContact
        fields = ('__all__')