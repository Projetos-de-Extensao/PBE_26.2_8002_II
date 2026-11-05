# app/api.py
from rest_framework import viewsets

from app.models import Aluno, FilaEspera, Profissional, Sala
from app.serializers import (
    AlunoSerializer,
    FilaEsperaSerializer,
    ProfissionalSerializer,
    SalaSerializer,
)


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class FilaEsperaViewSet(viewsets.ModelViewSet):
    queryset = FilaEspera.objects.all()
    serializer_class = FilaEsperaSerializer


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
