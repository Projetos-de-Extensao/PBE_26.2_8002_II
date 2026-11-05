# app/api.py
from rest_framework import viewsets

from app.models import Agendamento, Aluno, FilaEspera, Profissional, Sala, Turma
from app.serializers import (
    AgendamentoSerializer,
    AlunoSerializer,
    FilaEsperaSerializer,
    ProfissionalSerializer,
    SalaSerializer,
    TurmaSerializer,
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
    
class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    
class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
