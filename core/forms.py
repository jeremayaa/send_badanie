from django import forms
from .models import Pacjent, Badanie

class PacjentForm(forms.ModelForm):
    class Meta:
        model = Pacjent
        fields = ['pesel', 'imie', 'nazwisko', 'data_urodzenia', 'opis']

class BadanieForm(forms.ModelForm):
    class Meta:
        model = Badanie
        # na razie bez tagów – tylko pacjent, obraz i opis
        fields = ['pacjent', 'zdjecie', 'opis']