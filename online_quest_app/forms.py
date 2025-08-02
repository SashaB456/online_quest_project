from django import forms
from .models import Quiz, Question
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"
        exclude = ['user']
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ['user']