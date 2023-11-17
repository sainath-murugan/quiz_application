from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .admin_form import CustomUserCreationFormAdmin, CustomUserChangeFormAdmin
from .models import QRcode, LoginHistory, Ticket, AnonymousContact

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationFormAdmin
    form = CustomUserChangeFormAdmin
    model = CustomUser
    list_display = ['email',"username", 'is_staff', "is_active", "is_superuser",'last_login',]
    list_filter = ['email',"username", 'is_staff', "is_active", "is_superuser",'last_login']
    fieldsets = (
        (
            "username and email",
            {
                "fields": ("email", "username", "password",)
            }
        ), 
        (
            "personal info", 
            { 
                "fields" :("first_name" , "last_name")
            }      
        ),
        (
            "Permissions", 
            {
                "fields": ("is_staff", "is_active","is_superuser", "groups", "user_permissions")
            }
        ),
        (
            'Important dates', 
            {
                'fields': ('last_login', 'date_joined')
            }
        ),
        (
            "Password Reset Data",
            {
                'fields': ('password_reset_choices_qn', 'password_reset_choices_ans', 'password_reset_choices_verify')
            }
        ),
         (
            "account type (choose any one of this)",
            {
                'fields': ('account_type',)
            }
        ),
        (
            "Authenticator",
            {
                'fields': ('authenticator', 'authenticator_enable')
            }
        )
    ) #used to view user or change

    add_fieldsets = (
        (
            "username and email", 
            {
                "classes": ("wide",),
                "fields": ("email", "username",)
            }
        ),
        (
            "password", 
            {
                "classes": ("wide",),
                "fields": ("password1", "password2")
            }
        ),
        (
        "Permissions", 
            {
                "fields": ("is_staff", "is_active","is_superuser", "groups", "user_permissions")
            }
        ),
        (
            "account type (choose any one of this)",
            {
                "classes": ("wide",),
                'fields': ('account_type',)
            }
        ),
        (
            "Authenticator",
            {
                'fields': ('authenticator', 'authenticator_enable')
            }
        )
       
    )  #used in creating user
    search_fields = ("email", "username")
    ordering = ("email",)
    
    def get_readonly_fields(self, request, obj=None):
        
        if obj:  # Editing an existing instance
            return ('account_type',) 
        else:  # Creating a new instance
            return self.readonly_fields

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(QRcode)
admin.site.register(LoginHistory)
admin.site.register(Ticket)
admin.site.register(AnonymousContact)