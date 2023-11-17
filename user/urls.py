from django.urls import path
from . import views

app_name = "user"   

urlpatterns = [
    
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name= "login"),
    path("logout/", views.logout, name= "logout"),
    path("change_password/", views.changePassword, name= "change_password"),
    path("set_reset_password_question/", views.setResetPasswordQuestion, name="set_reset_password_question"),
    path("forgot_password/", views.forgotPassword, name="forgot_password"),
    path("reset_password/<uuid:id>/", views.resetPassword, name="reset_password"),
    path("reset_password_check_qn/<uuid:id>/", views.resetPasswordCheckQn, name="reset_password_check_qn"),
    path("profile/", views.profilePage, name="profile"),
    path("two_factor/", views.twoFactor, name="two_factor"),
    path("delete_login_history/", views.deleteLoginHistory, name="delete_login_history"),
    path("create_ticket/", views.createTicket, name="create_ticket"),
    path('anonymous_contact/', views.anonymousContact, name='anonymous_contact')
    
]