from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from One.models import UserProfileEducator, UserProfileStudent
import random
from .models import QRcode, LoginHistory
from django.contrib.auth.signals import user_logged_in
from user_agents import parse

@receiver(post_save, sender=CustomUser)
def user_created(sender, instance, created, **kwargs):
    
    if created:
        if instance.account_type == 'EDUCATOR':
            obj = UserProfileEducator.objects.create(user = instance)
            obj.save()
        elif instance.account_type == "STUDENT":
            obj = UserProfileStudent.objects.create(user = instance)
            obj.save()
        qr_code = random.choice(QRcode.objects.all())
        instance.authenticator = qr_code
        instance.save()
        
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
   
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    if user_agent.is_bot:
        obj = LoginHistory.objects.create(
            user = user,
            browser="No",
            device="No",
            bot= True
        )
        obj.save()
    else:
        obj = LoginHistory.objects.create(
            user = user,
            browser = user_agent.browser.family,
            device = f"{user_agent.os.family}",
            bot= False
        )
        obj.save()