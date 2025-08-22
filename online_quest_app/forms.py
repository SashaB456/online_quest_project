from django import forms
from .models import Quiz, Question, UserProfile
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'question']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["question"].queryset = Question.objects.filter(user=user)
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ['user']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ['user', 'role', 'banned', 'banned_date']