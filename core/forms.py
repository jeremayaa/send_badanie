from django import forms
from .models import Pacjent, Badanie, Analiza

class PacjentForm(forms.ModelForm):
    class Meta:
        model = Pacjent
        fields = ['pesel', 'imie', 'nazwisko', 'data_urodzenia', 'opis']

class BadanieForm(forms.ModelForm):
    class Meta:
        model = Badanie
        # na razie bez tagów – tylko pacjent, obraz i opis
        fields = ['pacjent', 'nazwa', 'zdjecie', 'opis']


class AnalizaForm(forms.ModelForm):
    class Meta:
        model = Analiza
        # badanie przypisujemy w form_valid, więc go nie pokazujemy
        fields = ['nazwa', 'zdjecie', 'opis']