from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.forms import SignUpForm
# Create your views here.
class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
