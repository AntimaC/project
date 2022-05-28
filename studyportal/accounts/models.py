from datetime import datetime
from django.db import models
from email.mime import image
from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,default="1", on_delete=models.CASCADE, related_name="profile")
   # user = models.OneToOneField(User,default="1", on_delete=models.CASCADE)   
    #forget_password_token = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images",default="default/user.png")
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(default=now)
    
    def __str__(self):
       return f'{self.user} profile'

   