from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Quiz, Question, UserProfile
from .forms import QuizForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
from random import shuffle
# Create your views here.

class QuizList(ListView):
    model = Quiz
    template_name = 'online_quest_app/quiz_list.html'
    context_object_name = 'quizzes'
    def get(self, request):
        super().get(request)
        return render(request, self.template_name, context=self.get_context_data())
    paginate_by = 3
class QuizCreate(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'online_quest_app/quiz_create.html'
    success_url = reverse_lazy('quiz-list')
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
class QuizEdit(LoginRequiredMixin, UpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'online_quest_app/quiz_create.html'
    def get_success_url(self):
        return reverse('quiz-edit', kwargs={"pk": self.get_object().pk})
class QuizDelete(LoginRequiredMixin, DeleteView):
    model = Quiz
    template_name = 'online_quest_app/quiz_delete.html'
    success_url = reverse_lazy('quiz-list')
def Challenge(request, quiz_id):
    score = 0
    quiz = Quiz.objects.get(id=quiz_id)
    request.session['quiz_id'] = quiz.id
    request.session['question_number'] = 1
    request.session['score'] = score

    return redirect('play-quiz', quiz_id=quiz_id, question_number=1)
def play_quiz(request, quiz_id, question_number=1):
    quiz = Quiz.objects.get(id=quiz_id)
    question_number = request.session.get('question_number', 1)
    questions = list(quiz.question.all())
    shuffle(questions)
    quiz_size = len(questions)
    current_question = questions[question_number - 1]
    if request.method == "POST":
        answer = request.POST.get('answer')
        correct_answer = current_question.correct_answer
        if answer.lower() == correct_answer.lower():
            request.session['score'] += 1
        if question_number < quiz_size:
            request.session['question_number'] = question_number + 1
            return redirect('play-quiz', quiz_id=quiz_id, question_number=request.session['question_number'])
        else:
            return redirect('results', quiz_id=quiz_id)
    #answers = current_question
    return render(request, 'online_quest_app/play_quiz.html', {
        'quiz': quiz,
        'question': current_question,
        'question_number': question_number,
        'quiz_size': quiz_size,
        'score': request.session.get('score'),
    })
def results(request, quiz_id):
    return render(request, 'online_quest_app/results.html', {
        'score': request.session.get('score'),
        'quiz': Quiz.objects.get(id=quiz_id),
        'quiz_len': request.session.get('question_number')
    })
class GetUserProfile(DetailView):
    model = UserProfile
    template_name = 'online_quest_app/user_profile.html'
    context_object_name = 'profile'