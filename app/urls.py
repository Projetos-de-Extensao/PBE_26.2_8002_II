from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.api import (
    AgendamentoViewSet,
    AlunoViewSet,
    #  OcupacaoViewSet,
    ProfissionalViewSet,
    RegistroTreinamentoViewSet,
    ResponsavelViewSet,
    SalaViewSet,
    ServicoViewSet,
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
# router.register(r"ocupacoes", OcupacaoViewSet, basename="ocupacao")
router.register(r"servicos", ServicoViewSet, basename="servico")

urlpatterns = [
    path("api/", include(router.urls)),
]
