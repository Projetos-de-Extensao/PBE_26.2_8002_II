from datetime import date

from django.db import models

class Sala(models.Model):
    id = models.TextField().primary_key
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    disponivel = models.BooleanField()

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    responsavel = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    

    def calcular_idade(self):
        hoje = date.today()
        nasc = self.data_nascimento
        return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

    def __str__(self):
        return self.nome
    
class FilaEspera(models.Model):
    id = models.TextField().primary_key
    posicao = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')

    def __str__(self):
        return self.id