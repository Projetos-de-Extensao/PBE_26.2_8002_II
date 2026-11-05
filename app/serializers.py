# app/serializers.py

from rest_framework import serializers

from app.models import Aluno, FilaEspera, Profissional, Responsavel, Sala


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "nome", "email", "senha"]
        extra_kwargs = {"senha": {"write_only": True}}


class ResponsavelSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = Responsavel
        fields = UsuarioSerializer.Meta.fields + ["telefone"]


class ProfissionalSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = Profissional
        fields = UsuarioSerializer.Meta.fields + ["especialidade"]


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ["id", "nome", "capacidade", "disponivel"]
        read_only_fields = ["id"]


class AlunoSerializer(serializers.ModelSerializer):
    idade = serializers.IntegerField(source="calcular_idade", read_only=True)

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
        read_only_fields = ["id"]

    def get_idade(self, obj):
        return obj.calcular_idade()


class FilaEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilaEspera
        fields = ["id", "posicao", "status"]
        read_only_fields = ["id"]

class AgendamentoSerializer(serializers.Serializer):
    aluno = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all())
    sala = serializers.PrimaryKeyRelatedField(queryset=Sala.objects.all())
    data_hora = serializers.DateTimeField()
    class Meta:
        fields = ['aluno', 'sala', 'data_hora']
        
class TurmaSerializer(serializers.Serializer):
    sala = serializers.PrimaryKeyRelatedField(queryset=Sala.objects.all())
    alunos = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all(), many=True)
    class Meta:
        fields = ['sala', 'alunos']