from enum import unique
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.forms import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utlis import profile
# Create your models here.
class Topic(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=500)
    image=models.URLField(max_length=200,default=None)
    wide_image=models.URLField(max_length=200,default=None)
    def __str__(self)->str:
        return str(self.id)+'.  '+self.title

class Choice(models.Model):
    class Meta:
        unique_together=(('topic','option_no'))
    id=models.IntegerField(primary_key=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    option_no=models.IntegerField(default=0)
    option=models.CharField(max_length=55)
    count=models.IntegerField(default=0)
    def __str__(self)->str:
        return str(self.id)+'.  '+self.option+'  '+str(self.topic)

class Reaction(models.Model):
    class Meta:
        unique_together=(('user','choice','topic'))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    time=models.DateTimeField()

class UserProfile (models.Model):
    profile_user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile_img  = models.ImageField(default='')

@receiver(post_save,sender=User)
def update_profile_signal (sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(profile_user=  instance)
    instance.userprofile.save()




