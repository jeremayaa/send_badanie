from django import forms
from .models import Pacjent, Badanie, Analiza, Tag

class PacjentForm(forms.ModelForm):
    class Meta:
        model = Pacjent
        fields = ['pesel', 'imie', 'nazwisko', 'data_urodzenia', 'opis']


from django.utils import timezone
class BadanieForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'}),
        initial=lambda: timezone.now().date()
    )

    class Meta:
        model = Badanie
        fields = ['pacjent', 'nazwa', 'data', 'zdjecie', 'opis', 'tagi']

    def __init__(self, *args, **kwargs):
        lekarz = kwargs.pop('lekarz', None)
        super().__init__(*args, **kwargs)

        if lekarz:
            self.fields['pacjent'].queryset = lekarz.pacjenci.all()

        self.fields['opis'].required = False
        self.fields['tagi'].required = False


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