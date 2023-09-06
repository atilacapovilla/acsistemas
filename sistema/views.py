from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sistema


def home(request):
    return render(request, 'home.html')


class SistemaList(LoginRequiredMixin,ListView):
    model = Sistema
    context_object_name = 'sistemas'
    template_name = 'sistema/sistema.html'
