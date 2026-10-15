# app/serializers.py
from rest_framework import serializers
from app.models import Sala

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nome', 'capacidade', 'disponivel']
        read_only_fields = ['id']
