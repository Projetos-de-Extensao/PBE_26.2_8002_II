# app/api.py
from rest_framework import viewsets

from app.models import Aluno, Sala
from app.serializers import AlunoSerializer, SalaSerializer


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
