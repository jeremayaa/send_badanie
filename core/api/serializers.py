from rest_framework import serializers
from core.models import Pacjent, Badanie, Analiza, Tag

class PacjentSerializer(serializers.ModelSerializer):
    latest_badanie = serializers.DateField(read_only=True)

    class Meta:
        model = Pacjent
        fields = ['id', 'pesel', 'imie', 'nazwisko', 'data_urodzenia', 'opis', 'lekarz', 'latest_badanie']

class BadanieSerializer(serializers.ModelSerializer):
    # tagi jako lista ID
    tagi = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )
    # class Meta:
    #     model = Badanie
    #     fields = [
    #         'id', 'pacjent', 'nazwa', 'zdjecie',
    #         'opis', 'data', 'tagi'
    #     ]
    #     read_only_fields = ['data']
    class Meta:
        model = Badanie
        fields = ['id', 'pacjent', 'nazwa', 'data', 'zdjecie', 'opis', 'tagi']

class AnalizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analiza
        fields = [
            'id', 'badanie', 'nazwa',
            'zdjecie', 'opis', 'data'
        ]
        read_only_fields = ['data']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nazwa']