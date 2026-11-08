from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.api import (
    AlunoViewSet,
    ProfissionalViewSet,
    SalaViewSet,
)
from app.views import index

router = DefaultRouter()
router.register(r"sala", SalaViewSet, basename="sala")
router.register(r"alunos", AlunoViewSet, basename="aluno")
router.register(r"profissional", ProfissionalViewSet, basename="profissional")

urlpatterns = [
    path("api/", include(router.urls)),
]
