from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Pacjent, Badanie, Analiza
from .serializers import PacjentSerializer, BadanieSerializer, AnalizaSerializer

class PacjentViewSet(viewsets.ModelViewSet):
    queryset = Pacjent.objects.all()
    serializer_class = PacjentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # przypisujemy lekarza z request.user
        serializer.save(lekarz=self.request.user.lekarz)

class BadanieViewSet(viewsets.ModelViewSet):
    serializer_class = BadanieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Badanie.objects.all()
        tagi = self.request.query_params.getlist('tagi')
        if tagi:
            qs = qs.filter(tagi__id__in=tagi).distinct()
        return qs



class AnalizaViewSet(viewsets.ModelViewSet):
    queryset = Analiza.objects.all()
    serializer_class = AnalizaSerializer
    permission_classes = [IsAuthenticated]
