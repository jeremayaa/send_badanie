from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Lekarz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # wykorzystujemy auth
    opis = models.TextField(blank=True)

class Pacjent(models.Model):
    lekarz = models.ForeignKey(Lekarz, on_delete=models.CASCADE, related_name='pacjenci')
    pesel = models.CharField(max_length=11, unique=True)
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    data_urodzenia = models.DateField()
    opis = models.TextField(blank=True)

class Tag(models.Model):
    nazwa = models.CharField(max_length=50, unique=True)
    opis = models.TextField(blank=True)

class Badanie(models.Model):
    pacjent = models.ForeignKey(Pacjent, on_delete=models.CASCADE, related_name='badania')
    tagi = models.ManyToManyField(Tag, related_name='badania', blank=True)
    zdjecie = models.ImageField(upload_to='badania/')
    opis = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

class Analiza(models.Model):
    badanie = models.ForeignKey(Badanie, on_delete=models.CASCADE, related_name='analizy')
    nazwa = models.CharField(max_length=100)
    zdjecie = models.ImageField(upload_to='analizy/')
    opis = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)