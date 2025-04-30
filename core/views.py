from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from .models import Pacjent, Badanie
from .forms import PacjentForm, BadanieForm



class PacjentListView(LoginRequiredMixin, ListView):
    model = Pacjent
    template_name = 'core/pacjent_list.html'
    context_object_name = 'pacjenci'


from django.urls import reverse_lazy

class PacjentCreateView(LoginRequiredMixin, CreateView):
    model = Pacjent
    form_class = PacjentForm
    template_name = 'core/pacjent_form.html'
    success_url = reverse_lazy('core:pacjent-list')

    def form_valid(self, form):
        form.instance.lekarz = self.request.user.lekarz
        return super().form_valid(form)

class BadanieListView(LoginRequiredMixin, ListView):
    model = Badanie
    template_name = 'core/badanie_list.html'
    context_object_name = 'badania'


class BadanieCreateView(LoginRequiredMixin, CreateView):
    model = Badanie
    form_class = BadanieForm
    template_name = 'core/badanie_form.html'
    success_url = reverse_lazy('core:badanie-list')

    def get_initial(self):
        initial = super().get_initial()
        pacjent_id = self.request.GET.get('pacjent')
        if pacjent_id and Pacjent.objects.filter(pk=pacjent_id).exists():
            initial['pacjent'] = pacjent_id
        return initial

class BadanieDetailView(LoginRequiredMixin, DetailView):
    model = Badanie
    template_name = 'core/badanie_detail.html'
    context_object_name = 'badanie'