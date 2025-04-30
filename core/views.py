from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Pacjent, Badanie

class PacjentListView(LoginRequiredMixin, ListView):
    model = Pacjent
    template_name = 'core/pacjent_list.html'
    context_object_name = 'pacjenci'

class BadanieListView(LoginRequiredMixin, ListView):
    model = Badanie
    template_name = 'core/badanie_list.html'
    context_object_name = 'badania'