from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.api import (
    AgendamentoViewSet,
    AlunoViewSet,
    ProfissionalViewSet,
    RegistroTreinamentoViewSet,
    ResponsavelViewSet,
    SalaViewSet,
)
from app.views import index

router = DefaultRouter()
router.register(r"profissionais", ProfissionalViewSet, basename="profissional")
router.register(r"responsaveis", ResponsavelViewSet, basename="responsavel")
router.register(r"alunos", AlunoViewSet, basename="aluno")
router.register(r"salas", SalaViewSet, basename="sala")
router.register(r"agendamentos", AgendamentoViewSet, basename="agendamento")
router.register(
    r"registros", RegistroTreinamentoViewSet, basename="registro-treinamento"
)

urlpatterns = [
    path("api/", include(router.urls)),
]
