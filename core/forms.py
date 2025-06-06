from django import forms
from .models import Pacjent, Badanie, Analiza, Tag

class PacjentForm(forms.ModelForm):
    class Meta:
        model = Pacjent
        fields = ['pesel', 'imie', 'nazwisko', 'data_urodzenia', 'opis']

# class BadanieForm(forms.ModelForm):
#     class Meta:
#         model = Badanie
#         # na razie bez tagów – tylko pacjent, obraz i opis
#         fields = ['pacjent', 'nazwa', 'zdjecie', 'opis']
from django.utils import timezone
class BadanieForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'}),
        initial=lambda: timezone.now().date()
    )

    class Meta:
        model = Badanie
        fields = ['pacjent', 'nazwa', 'data', 'zdjecie', 'opis', 'tagi']
        
class AnalizaStandardForm(forms.ModelForm):
    class Meta:
        model = Analiza
        fields = ['nazwa', 'zdjecie', 'opis']

class AnalizaProgramForm(forms.ModelForm):
    class Meta:
        model = Analiza
        fields = ['nazwa', 'zdjecie', 'opis']
        widgets = {
            # ukrywamy pole pliku, bo będziemy je wypełniać z JS
            'zdjecie': forms.ClearableFileInput(attrs={'style': 'display:none;'}),
        }