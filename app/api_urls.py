# app/api_urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.api import AlunoViewSet, SalaViewSet

router = DefaultRouter()
router.register(r"sala", SalaViewSet, basename="sala")
router.register(r"alunos", AlunoViewSet, basename="aluno")

urlpatterns = [
    path("", include(router.urls)),
]
