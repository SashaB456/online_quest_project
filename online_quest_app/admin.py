from django.contrib import admin
from .models import Role, UserProfile, Question, Quiz
# Register your models here.
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Quiz)