from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Quiz, Question, UserProfile
from .forms import QuizForm, QuestionForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
from random import shuffle
from django.contrib.auth.models import User
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
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["question"].queryset = Question.objects.filter(user=self.request.user)
        return form
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
        if form.instance.type == 'test':
            if form.instance.correct_answer in [form.instance.answer1, form.instance.answer2, form.instance.answer3, form.instance.answer4]:
                return super().form_valid(form)
            else:
                return HttpResponse(f"The correct answer must be any of the made options.", status=400)
        elif form.instance.type == 'open':
            return super().form_valid(form)
class QuizEdit(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'online_quest_app/quiz_create.html'
    def get_success_url(self):
        return reverse('quiz-edit', kwargs={"pk": self.get_object().pk})
class QuestionEdit(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'online_quest_app/quiz_create.html'
    def get_success_url(self):
        return reverse('question-edit', kwargs={"pk": self.get_object().pk})
class QuizDelete(LoginRequiredMixin, UserIsOwnerMixin,DeleteView):
    model = Quiz
    template_name = 'online_quest_app/quiz_delete.html'
    success_url = reverse_lazy('quiz-list')
class QuestionDelete(LoginRequiredMixin, UserIsOwnerMixin,DeleteView):
    model = Question
    template_name = 'online_quest_app/quiz_delete.html'
    success_url = reverse_lazy('question-list')
def Challenge(request, quiz_id):
    score = 0
    quiz = Quiz.objects.get(id=quiz_id)
    request.session['quiz_id'] = quiz.id
    request.session['question_number'] = 1
    request.session['score'] = score
    #request.session['shuffled'] = True

    return redirect('play-quiz', quiz_id=quiz_id, question_number=1)

def play_quiz(request:HttpRequest, quiz_id, question_number=1):
    quiz = Quiz.objects.get(id=quiz_id)
    question_number = request.session.get('question_number', 1)
    if 'questions_order' not in request.session or request.session.get('quiz_id') != quiz_id:
        questions = list(quiz.question.values_list('id', flat=True))
        shuffle(questions)
        request.session['questions_order'] = questions
        request.session['score'] = 0
        request.session['quiz_id'] = quiz.id
        request.session['question_number'] = 1

    questions_order = request.session.get('questions_order')
    quiz_size = len(questions_order)
    current_question_id = questions_order[question_number - 1]
    current_question = quiz.question.get(id=current_question_id)

    if request.method == "POST":
        answer = request.POST.get('answer')
        correct_answer = current_question.correct_answer
        if answer.lower() == correct_answer.lower():
            request.session['score'] += 1
        if question_number < quiz_size:
            request.session['question_number'] = question_number + 1
            return redirect('play-quiz', quiz_id=quiz_id, question_number=request.session['question_number'])
        else:
            del request.session['questions_order']
            return redirect('results', quiz_id=quiz_id)
    #answers = current_question
    return render(request, 'online_quest_app/play_quiz.html', {
        'quiz': quiz,
        'question': current_question,
        'question_number': question_number,
        'quiz_size': quiz_size,
        'score': request.session.get('score'),
        'questions_ids': questions_order
    })
def results(request, quiz_id):
    return render(request, 'online_quest_app/results.html', {
        'score': request.session.get('score'),
        'quiz': Quiz.objects.get(id=quiz_id),
        'quiz_len': request.session.get('question_number')
    })
class GetUserProfile(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'online_quest_app/user_profile.html'
    context_object_name = 'profile'
    def get_object(self):
        user = super().get_object()
        return user.profile
class UpdateUserProfile(UpdateView, UserIsOwnerMixin, LoginRequiredMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'online_quest_app/user_profile_update.html'
    context_object_name = 'profile'
    def get_object(self):
        user = super().get_object()
        return user.profile
    def get_success_url(self):
        return reverse('user-profile', kwargs={"pk": self.get_object().user.id})
def QuestionList(request):
    result = Question.objects.filter(user=request.user)
    if request.user.profile.role.name == 'Admin' or request.user.profile.role.name == 'Moderator':
        result = Question.objects.filter(user=request.user)
    return render(request, context={'questions': result}, template_name='online_quest_app/question_list.html')