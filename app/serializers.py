# app/serializers.py
from rest_framework import serializers
from datetime import date
from app.models import Sala, Aluno, FilaEspera

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nome', 'capacidade', 'disponivel']
        read_only_fields = ['id']

class AlunoSerializer(serializers.ModelSerializer):
    idade = serializers.SerializerMethodField()

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'data_nascimento', 'responsavel', 'ativo', 'idade']
        read_only_fields = ['id']

    def get_idade(self, obj):
        return obj.calcular_idade()



class FilaEsperaSerializer(serializers.ModelSerializer):
    idade = serializers.SerializerMethodField()

    class Meta:
        model = FilaEspera
        fields = ['id', 'posicao', 'status']
        read_only_fields = ['id']

