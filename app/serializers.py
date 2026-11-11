# app/serializers.py

from rest_framework import serializers

from app.models import (
    Agendamento,
    Aluno,
    # Ocupacao,
    Profissional,
    RegistroTreinamento,
    Responsavel,
    Sala,
    Servico,
)


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ["nome", "telefone", "cpf"]


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = ["id", "codigo_profissional", "nome", "ocupacao", "disponibilidade"]
        read_only_fields = ["id", "codigo_profissional"]


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = "__all__"


class AlunoSerializer(serializers.ModelSerializer):
    contato_responsavel = serializers.CharField(
        source="responsavel.telefone", read_only=True
    )
    nome_responsavel = serializers.CharField(source="responsavel.nome", read_only=True)

    class Meta:
        model = Aluno
        fields = [
            "id",
            "matricula",
            "nome",
            "data_nascimento",
            "responsavel",
            "nome_responsavel",
            "status",
            "idade",
            "contato_responsavel",
        ]
        read_only_fields = ["id", "responsavel", "matricula"]

    def validate_data_nascimento(self, value):
        if Aluno(data_nascimento=value).idade > 12:
            raise serializers.ValidationError(
                "A academia atende exclusivamente crianças até 12 anos de idade."
            )
        return value


class AgendamentoSerializer(serializers.ModelSerializer):
    posicao_fila = serializers.SerializerMethodField()
    aluno_matricula = serializers.SlugRelatedField(
        queryset=Aluno.objects.all(),
        slug_field="matricula",
        write_only=True,
        source="aluno",
    )
    aluno = serializers.StringRelatedField(read_only=True)
    profissional = serializers.StringRelatedField(read_only=True)
    sala = serializers.StringRelatedField(read_only=True)
    profissional_codigo = serializers.SlugRelatedField(
        queryset=Profissional.objects.all(),
        slug_field="codigo_profissional",  # Busca pelo código único
        write_only=True,
        source="profissional",
    )

    class Meta:
        model = Agendamento
        fields = [
            "id",
            "aluno",
            "aluno_matricula",
            "profissional_codigo",
            "profissional",
            "sala",
            "data_hora",
            "status",
            "posicao_fila",
            "criado_em",
        ]
        read_only_fields = [
            "status",
            "criado_em",
        ]

    def validate(self, attrs):
        sala_escolhida = attrs.get("sala")
        horario_escolhido = attrs.get("data_hora")
        if sala_escolhida is None or horario_escolhido is None:
            return attrs

        ocupacao_atual = Agendamento.objects.filter(
            sala=sala_escolhida, data_hora=horario_escolhido, status="ativo"
        ).count()

        if ocupacao_atual >= sala_escolhida.capacidade:
            attrs["status"] = "fila_espera"
        else:
            attrs["status"] = "ativo"

        return attrs

    def get_posicao_fila(self, obj):
        if obj.status != "fila_espera":
            return None

        pessoas_na_frente = Agendamento.objects.filter(
            sala=obj.sala,
            data_hora=obj.data_hora,
            status="fila_espera",
            criado_em__lt=obj.criado_em,
        ).count()

        return pessoas_na_frente + 1


class RegistroTreinamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroTreinamento
        fields = "__all__"
        read_only_fields = ["profissional"]


"""
class OcupacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocupacao
        fields = "__all__"
"""


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = "__all__"
