from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
# Create your views here.
class Registration(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect('quiz-list')