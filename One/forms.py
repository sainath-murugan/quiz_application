from django import forms
from .models import UserProfileEducator, College, UserProfileStudent, Course, QuestionForQuiz, Quiz
from django.utils import timezone
from datetime import timedelta

class UserProfileEducatorForm(forms.ModelForm):

    DOB = forms.DateField(
        label='',
        help_text="Enter your Date of birth",
        widget=forms.DateInput(
            attrs={
                'type': 'date', 
                'placeholder': 'select your date of birth'
            }
        ),
    )

    college_name = forms.ModelChoiceField(
        queryset=College.objects.all(), 
        label='',
        help_text="Select your college",
        widget=forms.Select(
            attrs={
                'placeholder': 'select your college'
            }
        ),
    )

    gender = forms.ChoiceField(
        choices=(
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("PREFER NOT TO TELL", "PREFER NOT TO TELL"),
        ),
        label='',
        help_text="select your gender",
        widget=forms.RadioSelect()
    )

    phone_number = forms.IntegerField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your phone number',
                'maxlength':10
            }
        ),
    )
    
    class Meta:

        model = UserProfileEducator
        fields = ('DOB', 'college_name', 'gender', 'phone_number')

    def clean_phone_number(self):

        phone_number = self.cleaned_data["phone_number"]
        if len(str(phone_number)) < 10:
            raise forms.ValidationError("enter your 10 digits phone number correctly")
        return phone_number

class UserProfileStudentForm(forms.ModelForm):

    DOB = forms.DateField(
        label='',
        help_text="Enter your Date of birth",
        widget=forms.DateInput(
            attrs={
                'type': 'date', 
                'placeholder': 'select your date of birth'
            }
        ),   
    )

    college_name = forms.ModelChoiceField(
        queryset=College.objects.all(), 
        label='',
        help_text="select your college_name",
        widget=forms.Select(
            attrs={
                'placeholder': 'select your college'
            }
        ), 
    )

    gender = forms.ChoiceField(
        choices=(
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("PREFER NOT TO TELL", "PREFER NOT TO TELL"),
        ),
        label='',
        widget=forms.RadioSelect(),
        help_text="Select your gender"
    )

    phone_number = forms.IntegerField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your phone number',
                'maxlength':10
            }
        ),
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), 
        label='',
        help_text="Select your course",
        widget=forms.Select(
            attrs={
                'placeholder': 'select your course'
            }
        ),
    )

    register_number = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your Register number'
            }
        ),
    )

    year = forms.ChoiceField(
        choices=(
        (1, "1"),
        (2, "2"),
        (3, '3'),
        (4, '4'),
        (5, '5')
        ),
        widget=forms.RadioSelect(),
        help_text="Select your year of study",
        label=''
    )

    class Meta:

        model = UserProfileStudent
        fields = ('DOB', 'college_name', 'gender', 'phone_number', 'course', 'register_number', 'year')

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if len(str(phone_number)) < 10:
            raise forms.ValidationError("enter your 10 digits phone number correctly")
        return phone_number

class QuizFormTitle(forms.ModelForm):

    title = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the title for your quiz'
            }
        ),
    )

    class Meta:

        model = Quiz
        fields = ("title",)

class QuizFormPublish(forms.ModelForm):
    
    start_time = forms.DateTimeField(
        label='',
        help_text="select time at which quiz should start",
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local', 
                'placeholder': 'select time at which quiz should start'
            }
        ),
    )

    student_dept = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(), 
        label='',
        widget=forms.CheckboxSelectMultiple(),
        help_text="Select your college",
    )
    
    year = forms.ChoiceField(
        choices=(
        (1, "1"),
        (2, "2"),
        (3, '3'),
        (4, '4'),
        (5, '5')
        ),
        widget=forms.RadioSelect(),
        help_text="Select your year to sent quiz",
        label=''
    )

    class Meta:

        model = Quiz
        fields = ("start_time",'student_dept', 'year')
    
    def clean_start_time(self):
        
        start_time = self.cleaned_data["start_time"]
        if start_time <= timezone.now() + timedelta(hours=1):
            raise forms.ValidationError("The test start time must be at least 1 hour in the future from current time.")
        else:
            return start_time
            
class CreateQuestion(forms.ModelForm):

    question = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your question'
            }
        ),
    )

    choice_one = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(         
            attrs={
                'class': 'form-control', 
                'placeholder': 'choice 1'
            }
        ),
    )

    choice_two = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'choice 2'
            }
        ),
    )

    choice_three = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'choice 3'
            }
        ),
    )

    choice_four = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'choice 4'
            }
        ),
    )

    ANS_CHOICE = [
        (1, "option 1"),
        (2, "option 2"),
        (3, "option 3"),
        (4, "option 4"),
    ]

    correct_ans = forms.ChoiceField(
        choices=ANS_CHOICE,
        help_text="select the correct choice for the above question",
        widget=forms.RadioSelect(),
        label=''   
    )

    class Meta:

        model = QuestionForQuiz
        fields = ("__all__")
        exclude=("quiz",)