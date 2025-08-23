from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField("auth.Permission")
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    banned = models.BooleanField(default=False)
    banned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Question(models.Model):
    question = models.TextField()
    types = [('open', 'Відкрите питання'), ('test', 'Тестове питання')]
    type = models.CharField(choices=types, default=types[1])
    answer1 = models.TextField(null=True, blank=True)
    answer2 = models.TextField(null=True, blank=True)
    answer3 = models.TextField(null=True, blank=True)
    answer4 = models.TextField(null=True, blank=True)
    correct_answer = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.question}'
    
class Quiz(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)
    def __str__(self):
        return f"{self.name} -- {self.user}"
    class Meta:
        verbose_name_plural = "Quizzes"