from django.db import models
from django.conf import settings
import uuid

class College(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    college_name = models.CharField(
        max_length=250,
        blank = False,  
    )

    state = models.CharField(
        max_length=100,
        blank = False,  
    )

    def __str__(self):

        return f"{self.college_name}"
    
class Course(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    course_name = models.CharField(
        max_length=250,
        blank = False,  
    )

    def __str__(self):
        
        return f"{self.course_name}"
    
class UserProfileEducator(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="user_profile_educator",
        unique=True,
        on_delete=models.CASCADE,
        null = True,
        blank=False
    )
    
    DOB = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null = True,
    )
    
    college_name = models.ForeignKey(
        College,
        on_delete= models.SET_NULL,  
        related_name="college_educator",
        null=True,
        blank=False,
    )

    CHOICE_GENDER = [
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("PREFER NOT TO TELL", "PREFER NOT TO TELL"),
    ]
        
    gender = models.CharField(
        max_length=50,
        choices=CHOICE_GENDER,
        blank = False
    )

    phone_number = models.IntegerField(
        blank=False,
        null = True
    )

    educator_profile_setup_verify = models.BooleanField(
        default=False,
        help_text="marked as verified, if profile setup is completed"
    )

    def __str__(self):
        
        return f"{self.user} | Active status: {self.user.is_active}"
        
    
    
class UserProfileStudent(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="user_profile_student",
        unique=True,
        on_delete=models.CASCADE,
        null = True,
        blank=False
    )
    
    DOB = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null = True,
        unique=False
    )
    
    college_name = models.ForeignKey(
        College,
        on_delete= models.SET_NULL,
        related_name="college_student",
        null=True,
        blank=False,
    )

    CHOICE_GENDER = [
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("PREFER NOT TO TELL", "PREFER NOT TO TELL"),
    ]
        
    gender = models.CharField(
        max_length=50,
        choices=CHOICE_GENDER,
        blank = False
    )

    phone_number = models.IntegerField(
        blank=False,
        null = True
    )

    course = models.ForeignKey(
        Course,
        on_delete= models.SET_NULL,
        related_name="course_enrolled",
        null=True,
        blank=False,
    )

    register_number = models.CharField(
        blank=False,
        max_length=50,
        default="",
    )

    YEAR_CHOICES=[
        (1, "1"),
        (2, "2"),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    year = models.IntegerField(
        null = True,
        choices=YEAR_CHOICES,
        blank = False
    )

    student_profile_setup_verify = models.BooleanField(
        default=False,
        help_text="marked as verified, if profile setup is completed"
    )
    
    def __str__(self):
        
        return f"{self.user}"
        
class Quiz(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(
        max_length=255,
        blank=False,
    )
    
    start_time = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null = True,
        help_text="don't change starting time while editing, it should be atleast one hour in future to attend the test"
    )
    
    created_by = models.OneToOneField( 
        UserProfileEducator,
        on_delete= models.CASCADE, 
        related_name="created_by_educator",
        null=True,
        blank=False,
    )

    student_dept = models.ManyToManyField(
        Course, 
        blank=False, 
        default='',
        help_text='quiz will be sent to this dept students',
    )
    
    YEAR_CHOICES=[
        (1, "1"),
        (2, "2"),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    
    year = models.IntegerField(
        null = True,
        choices=YEAR_CHOICES,
        blank = False
    )
    
    students_submitted = models.ManyToManyField(
        UserProfileStudent,
        blank=True,
        related_name="students_submitted_quiz",
    )

    submitted_verify = models.BooleanField(
        default=False,
        help_text="marked as verified, if all questions are submitted for this quiz (10 questions)"
    )

    publish_verify = models.BooleanField(
        default=False,
        help_text="marked as verified, if quiz is published"
    )

    def __str__(self):

        return self.title

class StudentMark(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    student = models.ForeignKey(
        UserProfileStudent,
        on_delete= models.CASCADE,  
        related_name="student_quiz_mark",
        null=True,
        blank=False,
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete= models.CASCADE,  
        related_name="student_quiz_attended",
        null=True,
        blank=False,
    )
    
    mark =  models.IntegerField(
        null = False,  
        blank = False,
        default=0
    )

    def __str__(self):

        return f"{self.student} | {self.mark}"

class QuestionForQuiz(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="question_created",
        null=True,
        blank=False
    )

    question = models.TextField()

    choice_one = models.CharField(
        max_length=255,
        blank = False,
    )

    choice_two = models.CharField(
        max_length=255,
        blank = False,
    )
    
    choice_three = models.CharField(
        max_length=255,
        blank = False,
    )
    
    choice_four = models.CharField(
        max_length=255,
        blank = False,
    )
    
    ANS_CHOICE = [
        (1, "option 1"),
        (2, "option 2"),
        (3, "option 3"),
        (4, "option 4"),
    ]

    correct_ans = models.IntegerField(
        blank = False,
        null=True,
        choices=ANS_CHOICE
    )

    def __str__(self):

        return self.question