# app/api_urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.api import AgendamentoViewSet, AlunoViewSet, FilaEsperaViewSet, ProfissionalViewSet, SalaViewSet, TurmaViewSet

router = DefaultRouter()
router.register(r"sala", SalaViewSet, basename="sala")
router.register(r"alunos", AlunoViewSet, basename="aluno")
router.register(r"fila-espera", FilaEsperaViewSet, basename="fila-espera")
router.register(r"profissional", ProfissionalViewSet, basename="profissional")
router.register(r"agendamento", AgendamentoViewSet, basename="agendamento")
router.register(r"turma", TurmaViewSet, basename="turma")

urlpatterns = [
    path("", include(router.urls)),
]
