from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Pacjent, Badanie, Analiza
from .serializers import PacjentSerializer, BadanieSerializer, AnalizaSerializer


from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
class PacjentViewSet(viewsets.ModelViewSet):
    # queryset = Pacjent.objects.all()
    serializer_class = PacjentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['imie','nazwisko','latest_badanie']
    ordering = ['nazwisko']  # domyślne

    def get_queryset(self):
        # zaczynamy od pełnego zbioru + adnotacja ostatniego badania
        qs = Pacjent.objects.annotate(
            latest_badanie=Max('badania__data')
        )
        # odczyt parametru scope (domyślnie 'mine')
        scope = self.request.query_params.get('scope', 'mine')
        if scope == 'mine':
            # tylko pacjenci zalogowanego lekarza
            return qs.filter(lekarz=self.request.user.lekarz)
        else:
            # wszyscy pacjenci
            return qs

    def perform_create(self, serializer):
        # przypisujemy lekarza z request.user
        serializer.save(lekarz=self.request.user.lekarz)

class BadanieViewSet(viewsets.ModelViewSet):
    serializer_class = BadanieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lekarz = getattr(self.request.user, 'lekarz', None)
        if not lekarz:
            return Badanie.objects.none()

        qs = Badanie.objects.filter(pacjent__lekarz=lekarz)

        # Optional filtering by tags (e.g., ?tagi=1&tagi=2)
        tagi = self.request.query_params.getlist('tagi')
        if tagi:
            qs = qs.filter(tagi__id__in=tagi).distinct()

        ordering = self.request.query_params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs




class AnalizaViewSet(viewsets.ModelViewSet):
    serializer_class = AnalizaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lekarz = getattr(self.request.user, 'lekarz', None)
        if not lekarz:
            return Analiza.objects.none()

        return Analiza.objects.filter(badanie__pacjent__lekarz=lekarz)