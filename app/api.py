from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import SAFE_METHODS, BasePermission

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
from app.serializers import (
    AgendamentoSerializer,
    AlunoSerializer,
    # OcupacaoSerializer,
    ProfissionalSerializer,
    RegistroTreinamentoSerializer,
    ResponsavelSerializer,
    SalaSerializer,
    ServicoSerializer,
    ServicoProfissionalSerializer,
)


class AdminEscreveTodosLeem(BasePermission):
    """Qualquer usuário logado consulta; só administrador altera."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class SalaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [AdminEscreveTodosLeem]


class AlunoViewSet(viewsets.ModelViewSet):
    serializer_class = AlunoSerializer

    def get_queryset(self):
        try:
            return Aluno.objects.filter(
                responsavel=self.request.user.perfil_responsavel
            )
        except Exception:
            return Aluno.objects.none()

    def perform_create(self, serializer):
        responsavel = getattr(self.request.user, "perfil_responsavel", None)
        if responsavel is None:
            raise PermissionDenied("Apenas responsáveis podem cadastrar alunos.")
        serializer.save(responsavel=responsavel)


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [AdminEscreveTodosLeem]

    def get_queryset(self):
        if hasattr(self.request.user, "perfil_responsavel"):
            return Profissional.objects.all()
        return Profissional.objects.filter(profile=self.request.user)

    def perform_create(self, serializer):
        if Profissional.objects.filter(profile=self.request.user).exists():
            raise ValidationError(
                "Este Profissional já está cadastrado na base de dados."
            )
        serializer.save(profile=self.request.user)


class AgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        try:
            responsavel_logado = self.request.user.perfil_responsavel
            return Agendamento.objects.filter(aluno__responsavel=responsavel_logado)
        except Exception:
            return Agendamento.objects.none()

    def perform_create(self, serializer):
        try:
            responsavel_logado = self.request.user.perfil_responsavel
            aluno_enviado = serializer.validated_data["aluno"]

            if aluno_enviado.responsavel != responsavel_logado:
                raise PermissionDenied(
                    "Você não tem permissão para agendar treinos para este aluno."
                )

            serializer.save()
        except AttributeError:
            raise PermissionDenied("Apenas responsáveis podem fazer agendamentos.")


class RegistroTreinamentoPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return hasattr(request.user, "profile_profissional")


class RegistroTreinamentoViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroTreinamentoSerializer
    permission_classes = [RegistroTreinamentoPermission]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "perfil_responsavel"):
            return RegistroTreinamento.objects.filter(
                agendamento__aluno__responsavel=user.perfil_responsavel
            )
        elif hasattr(user, "profile_profissional"):
            return RegistroTreinamento.objects.filter(
                profissional=user.profile_profissional
            )

        return RegistroTreinamento.objects.none()

    def perform_create(self, serializer):
        profissional_logado = getattr(self.request.user, "profile_profissional", None)
        if profissional_logado is None:
            raise PermissionDenied(
                "Apenas treinadores podem criar relatórios de treinamento."
            )
        serializer.save(profissional=profissional_logado)


class ResponsavelViewSet(viewsets.ModelViewSet):
    serializer_class = ResponsavelSerializer

    def get_queryset(self):

        return Responsavel.objects.filter(profile=self.request.user)

    def perform_create(self, serializer):
        if Responsavel.objects.filter(profile=self.request.user).exists():
            raise ValidationError("Este usuário já possui um perfil de responsável.")
        serializer.save(profile=self.request.user)


"""
class OcupacaoViewSet(viewsets.ModelViewSet):
    serializer_class = OcupacaoSerializer
    queryset = Ocupacao.objects.all()
    permission_classes = [AdminEscreveTodosLeem]
"""


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServicoSerializer
    queryset = Servico.objects.all()
    permission_classes = [AdminEscreveTodosLeem]

    def get_serializer_class(self):
        if self.action == "adicionar_profissional":
            return ServicoProfissionalSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="profissionais")
    def adicionar_profissional(self, request, pk=None):
        servico = self.get_object()
        serializer = ServicoProfissionalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profissional = serializer.validated_data["profissional"]

        if servico.profissionais.filter(pk=profissional.pk).exists():
            raise serializers.ValidationError(
                "Este profissional já está associado ao serviço."
            )

        servico.profissionais.add(profissional)
        return Response(
            {
                "detail": "Profissional associado ao serviço com sucesso.",
                "servico": servico.nome,
                "profissional": profissional.codigo_profissional,
            },
            status=201,
        )
