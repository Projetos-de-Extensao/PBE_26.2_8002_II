from datetime import date

from django.db import models


class Sala(models.Model):
    id = models.TextField().primary_key
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    disponivel = models.BooleanField()

    def __str__(self):
        return str(self.nome)


class Usuario(models.Model):
    nome = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=8, null=False)

    class Meta:
        abstract = True


class Responsavel(Usuario):
    telefone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Responsavel: {self.nome}"


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    responsavel_aluno = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, blank=False, null=False
    )
    ativo = models.BooleanField()
    status = models.CharField(
        max_length=20,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )

    def calcular_idade(self):
        hoje = date.today()
        nasc = self.data_nascimento
        return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

    def __str__(self):
        return str(self.nome)


class FilaEspera(models.Model):
    id = models.TextField().primary_key
    posicao = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )

    def __str__(self):
        return str(self.id)


class Profissional(Usuario):
    especialidade = (models.CharField(max_length=50),)
    disponibilidade = models.BooleanField()

    def __str__(self):
        return f"profissional: {self.nome}"
