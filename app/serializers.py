# app/serializers.py

from rest_framework import serializers

from app.models import (
    Agendamento,
    Aluno,
    Profissional,
    RegistroTreinamento,
    Responsavel,
    Sala,
)


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ["nome", "telefone", "cpf"]


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = ["id", "nome", "profile", "ocupacao", "disponibilidade"]


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = "__all__"


class AlunoSerializer(serializers.ModelSerializer):
    contato_responsavel = serializers.CharField(
        source="responsavel.telefone", read_only=True
    )

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "data_nascimento",
            "responsavel",
            "status",
            "idade",
            "contato_responsavel",
        ]
        read_only_fields = ["id", "responsavel"]

    def validate_data_nascimento(self, value):
        if Aluno(data_nascimento=value).idade > 12:
            raise serializers.ValidationError(
                "A academia atende exclusivamente crianças até 12 anos de idade."
            )
        return value


class AgendamentoSerializer(serializers.ModelSerializer):
    posicao_fila = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = [
            "id",
            "aluno",
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
