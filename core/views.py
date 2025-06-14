from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View, TemplateView
from .models import Pacjent, Badanie, Analiza, Tag
from .forms import PacjentForm, BadanieForm, AnalizaStandardForm, AnalizaProgramForm
from django.shortcuts import get_object_or_404


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'core/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the new user
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('core:pacjent-list')  # or wherever you want
        return render(request, 'core/register.html', {'form': form})

class PacjentListView(LoginRequiredMixin, ListView):
    model = Pacjent
    template_name = 'core/pacjent_list.html'
    context_object_name = 'pacjenci'

    def get_queryset(self):
        scope = self.request.GET.get('scope', 'all')
        if scope == 'mine':
            # tylko pacjenci zalogowanego lekarza
            return Pacjent.objects.filter(lekarz=self.request.user.lekarz)
        else:
            # wszyscy pacjenci
            return Pacjent.objects.all()
            # return None


from django.urls import reverse_lazy

class PacjentCreateView(LoginRequiredMixin, CreateView):
    model = Pacjent
    form_class = PacjentForm
    template_name = 'core/pacjent_form.html'
    success_url = reverse_lazy('core:pacjent-list')

    def form_valid(self, form):
        form.instance.lekarz = self.request.user.lekarz
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('core:pacjent-detail', kwargs={'pk': self.object.pk})
    
class PacjentDetailView(LoginRequiredMixin, DetailView):
    model = Pacjent
    template_name = 'core/pacjent_detail.html'
    context_object_name = 'pacjent'

    # def get_queryset(self):
    #     return Pacjent.objects.filter(lekarz=self.request.user.lekarz)
    

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

class PacjentUpdateView(LoginRequiredMixin, UpdateView):
    model = Pacjent
    form_class = PacjentForm
    template_name = 'core/pacjent_form.html'

    def get_queryset(self):
        return Pacjent.objects.filter(lekarz=self.request.user.lekarz)

    def get_success_url(self):
        return reverse('core:pacjent-detail', kwargs={'pk': self.object.pk})

class PacjentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        pacjent = get_object_or_404(Pacjent, pk=pk, lekarz=request.user.lekarz)
        pacjent.delete()
        # alert i redirect do listy
        url = reverse('core:pacjent-list')
        return HttpResponse(f"""
          <script>
            alert('Pacjent został usunięty');
            window.location.href = '{url}';
          </script>
        """)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Badanie, Tag

class BadanieListView(LoginRequiredMixin, ListView):
    model = Badanie
    template_name = 'core/badanie_list.html'
    context_object_name = 'badania'

    def get_queryset(self):
        user = self.request.user
        lekarz = getattr(user, 'lekarz', None)
        if not lekarz:
            return Badanie.objects.none()  # Only lekarze can see badania

        # Base queryset: only badania linked to user's own patients
        qs = Badanie.objects.filter(pacjent__lekarz=lekarz)

        # Filter by tags if provided
        tag_ids = self.request.GET.getlist('tags')  # ex: ?tags=1&tags=2
        if tag_ids:
            qs = qs.filter(tagi__in=tag_ids).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_tags'] = Tag.objects.all()
        ctx['selected_tags'] = list(map(int, self.request.GET.getlist('tags')))
        return ctx



class BadanieCreateView(LoginRequiredMixin, CreateView):
    model = Badanie
    form_class = BadanieForm
    template_name = 'core/badanie_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['lekarz'] = self.request.user.lekarz  # pass to form
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        pacjent_id = self.request.GET.get('pacjent')
        if pacjent_id and Pacjent.objects.filter(pk=pacjent_id, lekarz=self.request.user.lekarz).exists():
            initial['pacjent'] = pacjent_id
        return initial

    def get_success_url(self):
        return reverse('core:badanie-detail', kwargs={'pk': self.object.pk})


class BadanieDetailView(LoginRequiredMixin, DetailView):
    model = Badanie
    template_name = 'core/badanie_detail.html'
    context_object_name = 'badanie'

class BadanieUpdateView(LoginRequiredMixin, UpdateView):
    model = Badanie
    form_class = BadanieForm

    template_name = 'core/badanie_form.html'
    def get_queryset(self):
        # tylko badania pacjentów Twojego lekarza
        return Badanie.objects.filter(pacjent__lekarz=self.request.user.lekarz)

    def get_success_url(self):
        return reverse('core:badanie-detail', kwargs={'pk': self.object.pk})
    

class BadanieDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        badanie = get_object_or_404(
            Badanie, pk=pk, pacjent__lekarz=request.user.lekarz
        )
        badanie.delete()
        url = reverse('core:badanie-list')
        return HttpResponse(f"""
          <script>
            alert('Badanie zostało usunięte');
            window.location.href = '{url}';
          </script>
        """)
    

class AnalizaCreateView(LoginRequiredMixin, CreateView):
    """Standardowy formularz: nazwa, plik do wrzucenia, opis."""
    model = Analiza
    form_class = AnalizaStandardForm
    template_name = 'core/analiza_form.html'

    def form_valid(self, form):
        badanie = get_object_or_404(Badanie, pk=self.kwargs['badanie_pk'])
        form.instance.badanie = badanie
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:analiza-detail', kwargs={'pk': self.object.pk})
    
class AnalizaProgramCreateView(LoginRequiredMixin, CreateView):
    """Formularz programowy: auto-załadowany plik + zmiana nazwy."""
    model = Analiza
    form_class = AnalizaProgramForm
    template_name = 'core/analiza_program_form.html'

    def form_valid(self, form):
        badanie = get_object_or_404(Badanie, pk=self.kwargs['badanie_pk'])
        form.instance.badanie = badanie
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:analiza-detail', kwargs={'pk': self.object.pk})

class AnalizaDetailView(LoginRequiredMixin, DetailView):
    model = Analiza
    template_name = 'core/analiza_detail.html'
    context_object_name = 'analiza'

class AnalizaUpdateView(LoginRequiredMixin, UpdateView):
    model = Analiza
    form_class = AnalizaStandardForm
    template_name = 'core/analiza_form.html'

    def get_queryset(self):
        # tylko analizy badań Twojego lekarza
        return Analiza.objects.filter(
            badanie__pacjent__lekarz=self.request.user.lekarz
        )

    def get_success_url(self):
        return reverse('core:analiza-detail', kwargs={'pk': self.object.pk})

class AnalizaDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        analiza = get_object_or_404(
            Analiza, pk=pk,
            badanie__pacjent__lekarz=request.user.lekarz
        )
        analiza.delete()
        url = reverse('core:badanie-detail', kwargs={'pk': analiza.badanie.pk})
        return HttpResponse(f"""
          <script>
            alert('Analiza została usunięta');
            window.location.href = '{url}';
          </script>
        """)



class ProgramAnalyzeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/program_analyze.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'analiza_pk' in self.kwargs:
            analiza = get_object_or_404(Analiza, pk=self.kwargs['analiza_pk'])
            badanie = analiza.badanie
            ctx['base_image_url']    = badanie.zdjecie.url
            ctx['overlay_image_url'] = analiza.zdjecie.url
            ctx['redirect_url']      = reverse(
                'core:analiza-edit-program',
                kwargs={'pk': analiza.pk}
            )
            ctx['mode'] = 'edit'
        else:
            badanie = get_object_or_404(Badanie, pk=self.kwargs['badanie_pk'])
            ctx['base_image_url'] = badanie.zdjecie.url
            ctx['overlay_image_url'] = None
            ctx['redirect_url']      = reverse(
                'core:analiza-add-program',
                kwargs={'badanie_pk': badanie.pk}
            )
            ctx['mode'] = 'new'
        ctx['title'] = badanie.nazwa
        return ctx

class AnalizaProgramUpdateView(LoginRequiredMixin, UpdateView):
    """Formularz edycji analizy: auto-załadowany plik + zmiana nazwy."""
    model = Analiza
    form_class = AnalizaProgramForm
    template_name = 'core/analiza_program_form.html'

    def get_queryset(self):
        # tylko analizy Twoich pacjentów
        return Analiza.objects.filter(
            badanie__pacjent__lekarz=self.request.user.lekarz
        )

    def get_success_url(self):
        return reverse('core:analiza-detail', kwargs={'pk': self.object.pk})