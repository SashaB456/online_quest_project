from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from .models import Quiz, Question
from .forms import QuizForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
# Create your views here.

class QuizList(ListView):
    model = Quiz
    template_name = 'online_quest_app/quiz_list.html'
    context_object_name = 'quizzes'
    def get(self, request):
        super().get(request)
        return render(request, self.template_name, context=self.get_context_data())
class QuestionList(ListView):
    model = Question
    template_name = 'online_quest_app/question_list.html'
    context_object_name = 'questions'
    def get(self, request):
        super().get(request)
        return render(request, self.template_name, context=self.get_context_data())
class QuizDetail(DetailView):
    model = Quiz
    template_name = 'online_quest_app/quiz_detail.html'
    context_object_name = 'quiz'
class QuizCreate(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'online_quest_app/quiz_create.html'
    success_url = reverse_lazy('quiz-list')
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'online_quest_app/quiz_create.html'
    success_url = reverse_lazy('quiz-list')
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
class QuizDelete(LoginRequiredMixin, DeleteView):
    model = Quiz
    template_name = 'online_quest_app/quiz_delete.html'
    success_url = reverse_lazy('quiz-list')