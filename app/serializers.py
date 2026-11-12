# app/serializers.py

from datetime import timedelta

from django.utils import timezone
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
    SERVICO_SALA,
)


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ["id", "nome", "telefone", "cpf"]
        read_only_fields = ["id"]


class ProfissionalSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(
        source="codigo_profissional", read_only=True
    )
    formacao = serializers.CharField(source="ocupacao", read_only=True)

    class Meta:
        model = Profissional
        fields = [
            "id",
            "codigo_profissional",
            "matricula",
            "nome",
            "ocupacao",
            "formacao",
            "disponibilidade",
        ]
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
        if Aluno(data_nascimento=value).idade < 7:
            raise serializers.ValidationError(
                "A academia atende exclusivamente crianças a partir de 7 anos de idade."
            )
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
    servico = serializers.StringRelatedField(read_only=True)
    servico_nome = serializers.SlugRelatedField(
        queryset=Servico.objects.all(),
        slug_field="nome",
        write_only=True,
        source="servico",
    )
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
            "servico",
            "servico_nome",
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
        servico_escolhido = attrs.get(
            "servico", getattr(self.instance, "servico", None)
        )
        if servico_escolhido is not None:
            nome_sala = SERVICO_SALA[servico_escolhido.nome]
            sala_automatica = Sala.objects.filter(nome=nome_sala).first()
            if sala_automatica is None:
                raise serializers.ValidationError(
                    "A sala padrão do serviço ainda não foi cadastrada."
                )
            attrs["sala"] = sala_automatica

        aluno_escolhido = attrs.get("aluno", getattr(self.instance, "aluno", None))
        profissional_escolhido = attrs.get(
            "profissional", getattr(self.instance, "profissional", None)
        )
        sala_escolhida = attrs.get("sala", getattr(self.instance, "sala", None))
        horario_escolhido = attrs.get(
            "data_hora", getattr(self.instance, "data_hora", None)
        )
        if (
            aluno_escolhido is None
            or profissional_escolhido is None
            or sala_escolhida is None
            or horario_escolhido is None
            or servico_escolhido is None
        ):
            return attrs

        inicio = horario_escolhido
        fim = inicio + timedelta(minutes=servico_escolhido.duracao_minutos)
        agendamentos_existentes = Agendamento.objects.filter(
            status__in=["ativo", "fila_espera"]
        ).select_related("servico")
        if self.instance is not None:
            agendamentos_existentes = agendamentos_existentes.exclude(
                pk=self.instance.pk
            )

        for agendamento in agendamentos_existentes.filter(aluno=aluno_escolhido):
            inicio_existente = agendamento.data_hora
            fim_existente = inicio_existente + timedelta(
                minutes=agendamento.servico.duracao_minutos
            )
            if inicio < fim_existente and inicio_existente < fim:
                raise serializers.ValidationError(
                    {"data_hora": "O aluno já possui um agendamento neste intervalo."}
                )

        for agendamento in agendamentos_existentes.filter(
            profissional=profissional_escolhido
        ):
            inicio_existente = agendamento.data_hora
            fim_existente = inicio_existente + timedelta(
                minutes=agendamento.servico.duracao_minutos
            )
            if inicio < fim_existente and inicio_existente < fim:
                raise serializers.ValidationError(
                    {
                        "data_hora": (
                            "O profissional já possui um agendamento neste intervalo."
                        )
                    }
                )

        ocupacao_atual = 0
        for agendamento in agendamentos_existentes.filter(
            sala=sala_escolhida, status="ativo"
        ):
            inicio_existente = agendamento.data_hora
            fim_existente = inicio_existente + timedelta(
                minutes=agendamento.servico.duracao_minutos
            )
            if inicio < fim_existente and inicio_existente < fim:
                ocupacao_atual += 1

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


class AgendamentoMatriculaField(serializers.RelatedField):
    default_error_messages = {
        "does_not_exist": "Não existe agendamento para esta matrícula.",
        "multiple": "A matrícula possui mais de um agendamento; selecione o agendamento por outro meio.",
    }

    def to_internal_value(self, data):
        agendamentos = self.get_queryset().filter(aluno__matricula=data)
        if not agendamentos.exists():
            self.fail("does_not_exist")
        if agendamentos.count() > 1:
            self.fail("multiple")
        return agendamentos.get()

    def to_representation(self, value):
        return value.aluno.matricula


class RegistroTreinamentoSerializer(serializers.ModelSerializer):
    agendamento = AgendamentoMatriculaField(queryset=Agendamento.objects.all())

    def validate(self, attrs):
        agendamento = attrs.get(
            "agendamento", getattr(self.instance, "agendamento", None)
        )
        if agendamento is not None and agendamento.data_hora > timezone.now():
            raise serializers.ValidationError(
                {
                    "agendamento": (
                        "O registro só pode ser criado após o horário do treinamento."
                    )
                }
            )
        return attrs

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


class ServicoProfissionalSerializer(serializers.Serializer):
    profissional_codigo = serializers.SlugRelatedField(
        queryset=Profissional.objects.all(),
        slug_field="codigo_profissional",
        source="profissional",
    )
