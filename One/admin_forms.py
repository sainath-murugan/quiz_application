from django import forms
from .models import QuestionForQuiz, UserProfileEducator, College, UserProfileStudent, Course, Quiz

class CreateQuestionModelAdmin(forms.ModelForm):

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
    )

    class Meta:

        model = QuestionForQuiz
        fields = ("__all__")

class UserProfileEducatorFormAdmin(forms.ModelForm):


    gender = forms.ChoiceField(
        choices=(
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("PREFER NOT TO TELL", "PREFER NOT TO TELL"),
        ),
        help_text="select your gender",
        widget=forms.RadioSelect()
    )

    phone_number = forms.IntegerField(
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
        fields = ('__all__')

    def clean_phone_number(self):

        phone_number = self.cleaned_data["phone_number"]
        if len(str(phone_number)) < 10:
            raise forms.ValidationError("enter your 10 digits phone number correctly")
        return phone_number
        
class UserProfileStudentFormAdmin(forms.ModelForm):

    gender = forms.ChoiceField(
        choices=(
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("PREFER NOT TO TELL", "PREFER NOT TO TELL"),
        ),
        widget=forms.RadioSelect(),
        help_text="Select your gender"
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
        help_text="Select your year of study"
    )

    phone_number = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your phone number',
                'maxlength':10
            }
        ),
    )

    class Meta:

        model = UserProfileStudent
        fields = ('__all__')

    def clean_phone_number(self):

        phone_number = self.cleaned_data["phone_number"]
        if len(str(phone_number)) < 10:
            raise forms.ValidationError("enter your 10 digits phone number correctly")
        return phone_number
    
class QuizFormAdmin(forms.ModelForm):

    student_dept = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
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
    )

    students_submitted = forms.ModelMultipleChoiceField(
        queryset=UserProfileStudent.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        help_text="It displays all students attened quiz, irrespective of all colleges",         
    )

    students_submitted.required = False

    class Meta:

        model = Quiz
        fields = ("__all__")