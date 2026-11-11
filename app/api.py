from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from app.models import (
    Agendamento,
    Aluno,
    Profissional,
    RegistroTreinamento,
    Responsavel,
    Sala,
)
from app.serializers import (
    AgendamentoSerializer,
    AlunoSerializer,
    ProfissionalSerializer,
    RegistroTreinamentoSerializer,
    ResponsavelSerializer,
    SalaSerializer,
)


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


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
        try:
            serializer.save(responsavel=self.request.user.perfil_responsavel)
        except Exception:
            raise PermissionDenied("Apenas responsáveis podem cadastrar alunos.")


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


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
        elif hasattr(user, "perfil_profissional"):
            return RegistroTreinamento.objects.filter(
                profissional=user.perfil_profissional
            )

        return RegistroTreinamento.objects.none()

    def perform_create(self, serializer):
        try:
            profissional_logado = self.request.user.perfil_profissional
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

        serializer.save(profile=self.request.user)
