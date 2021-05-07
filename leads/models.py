from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)

class Lead(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 30)
    age = models.IntegerField(default = 0)

    agent = models.ForeignKey("Agent", default = "Agent 1", on_delete=models.CASCADE)
     
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) 

    def __str__(self):
        return self.user.email
