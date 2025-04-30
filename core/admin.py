from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Lekarz, Pacjent, Tag, Badanie, Analiza

admin.site.register(Lekarz)
admin.site.register(Pacjent)
admin.site.register(Tag)
admin.site.register(Badanie)
admin.site.register(Analiza)