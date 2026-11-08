# app/serializers.py

from rest_framework import serializers

from app.models import Aluno, Profissional, Responsavel, Sala


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "nome", "email", "senha"]
        extra_kwargs = {"senha": {"write_only": True}}


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ["nome", "telefone"]


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = ["especialidade"]


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ["id", "nome", "capacidade", "disponivel"]
        read_only_fields = ["id"]


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "data_nascimento",
            "responsavel_aluno",
            "ativo",
            "idade",
        ]
        read_only_fields = ["id", "responsavel_aluno"]
