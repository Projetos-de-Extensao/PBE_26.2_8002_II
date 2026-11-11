from rest_framework import viewsets
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
)


class AdminEscreveTodosLeem(BasePermission):
    """Qualquer usuário logado consulta; só administrador altera."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class SalaViewSet(viewsets.ModelViewSet):
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


class RegistroTreinamentoViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroTreinamentoSerializer

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
        try:
            profissional_logado = self.request.user.profile_profissional
            serializer.save(profissional=profissional_logado)
        except Exception:
            raise PermissionDenied(
                "Apenas treinadores podem criar relatórios de treinamento."
            )


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


class ServicoViewSet(viewsets.ModelViewSet):
    serializer_class = ServicoSerializer
    queryset = Servico.objects.all()
    permission_classes = [AdminEscreveTodosLeem]
