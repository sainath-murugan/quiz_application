from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .managers import CustomUserManager
from django.conf import settings

class QRcode(models.Model):

    authenticator_qrcode = models.ImageField(null=True, blank=True, upload_to='user_authenticator_qrcode_image')
    authenticator_secret_code = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.authenticator_secret_code}"
    
class CustomUser(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    username = models.CharField(max_length=200, blank=True)

    email = models.EmailField("email address", unique=True) 

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    object = CustomUserManager() 

    CHOICE_FOR_RESET_PASSWORD = [
        ("YOUR LUCKEY NUMBER", "YOUR LUCKEY NUMBER"), 
        ("YOUR BEST FRIEND NAME", "YOUR BEST FRIEND NAME"),
        ("YOUR FAVOURITE FOOD", "YOUR FAVOURITE FOOD"),
        ("YOUR FAVOURITE DESTINATION", "YOUR FAVOURITE DESTINATION")
    ]
        
    password_reset_choices_qn = models.CharField(
        max_length=50,
        choices=CHOICE_FOR_RESET_PASSWORD,
        default=CHOICE_FOR_RESET_PASSWORD[0]
    )
    
    password_reset_choices_ans = models.CharField(
        max_length=100,
        blank = False,
        default="",    
    )

    password_reset_choices_verify = models.BooleanField(
        default=False,
        help_text="marked as verified, if user cretaed reset password question"
    )

    ACCOUNT_TYPE = [
        ("EDUCATOR", "EDUCATOR"),
        ("STUDENT", "STUDENT"),
    ]
        
    account_type = models.CharField(
        max_length=50,
        choices=ACCOUNT_TYPE,
        blank = False,
        default=''
    )
    
    authenticator = models.ForeignKey(
        QRcode,
        related_name='user_qrcode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    authenticator_enable = models.BooleanField(
        default=False,
        help_text="marked as verified, if 2FA is enabled"
    )

    def __str__(self):

        return self.email
    
class LoginHistory(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_history",
        on_delete=models.CASCADE,
        null = True,
        blank=False
    )
    
    browser = models.CharField(
        max_length=255,
        blank=False,
    )
    
    device = models.CharField(
        max_length=255,
        blank=False,
    )
    
    bot = models.BooleanField(
        default=False,
        help_text="marked as verified, if it is bot"
    )

    logged_in = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        blank=False,
        null = True,
    )
    
    def __str__(self):

        return f"{self.user}"
    
class Ticket(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="user_ticket",
        on_delete=models.CASCADE,
        null = True,
        blank=False
    )

    title = models.CharField(
        max_length=255,
        blank=False,
    )

    message = models.TextField()

    def __str__(self):

        return f"{self.user.email} | {self.message}"

class AnonymousContact(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(
       blank=False,
       null=False 
    )

    title = models.CharField(
        max_length=255,
        blank=False,
    )

    message = models.TextField()

    def __str__(self):

        return f"{self.email} | {self.message}"