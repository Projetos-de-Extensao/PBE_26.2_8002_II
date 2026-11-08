from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Sala(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    disponivel = models.BooleanField()

    def __str__(self):
        return str(self.nome)


class Responsavel(models.Model):
    profile = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profiles"
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nome)


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    responsavel_aluno = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, blank=False, null=False
    )
    status = models.CharField(
        max_length=20,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )

    @property
    def idade(self):
        hoje = date.today()
        nasc = self.data_nascimento
        return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

    def __str__(self):
        return str(self.nome)

    def clean(self):
        if self.idade > 12:
            raise ValidationError(
                "A academia atende exclusivamente crianças até 12 anos de idade."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Garante que a validação roda!
        super().save(*args, **kwargs)


class FilaEspera(models.Model):
    posicao = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )

    def __str__(self):
        return str(self.id)


class Profissional(models.Model):
    especialidade = (models.CharField(max_length=50),)
    disponibilidade = models.BooleanField()

    def __str__(self):
        return str(self.nome)


class Servico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    duracao_minutos = models.IntegerField(default=30)  # type: ignore
    profissionais = models.ManyToManyField(Profissional, related_name="servicos")

    def __str__(self):
        return str(self.nome)


class Agendamento(models.Model):
    data_hora = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )

    turma = models.ForeignKey("Turma", on_delete=models.CASCADE, blank=True, null=True)
    servico = models.ForeignKey(
        Servico, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"Agendamento: {self.id}"


class Turma(models.Model):
    nome = models.CharField(max_length=100)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Aluno)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nome)
