from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

DISPONIBILIDADE_PROFISSIONAL = [
    ("DISPONIVEL", "disponivel"),
    ("INDISPONIVEL", "indisponivel"),
]


class Sala(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    disponivel = models.BooleanField()

    def __str__(self):
        return str(self.nome)


class Responsavel(models.Model):
    profile = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil_responsavel"
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nome)


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="alunos",
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
        return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))  # type: ignore

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


class Ocupacao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.nome)


class Profissional(models.Model):
    profile = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_profissional"
    )
    nome = models.CharField(max_length=150)
    ocupacao = models.ForeignKey(
        Ocupacao, on_delete=models.CASCADE, related_name="ocupacoes"
    )
    disponibilidade = models.CharField(
        max_length=20, choices=DISPONIBILIDADE_PROFISSIONAL, default="DISPONIVEL"
    )

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
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="agendamentos"
    )
    profissional = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="agendamentos"
    )
    status = models.CharField(
        max_length=20,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, blank=True, null=True)
    servico = models.ForeignKey(
        Servico, on_delete=models.CASCADE, blank=True, null=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agendamento: {self.id}"  # type: ignore


class RegistroTreinamento(models.Model):
    agendamento = models.OneToOneField(
        Agendamento, on_delete=models.CASCADE, related_name="registro_treinamento"
    )
    profissional = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="registros_criados"
    )

    presenca = models.CharField(max_length=50)
    observacoes = models.TextField()
    avaliacao_fisica = models.TextField()
    avaliacao_tecnica = models.TextField()

    def __str__(self):
        return f"Treino de {self.agendamento.aluno.nome} por {self.profissional.nome}"


"""
 class Turma(models.Model):
    modalidade = models.CharField(max_length=100)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Aluno)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    faixa_etaria_min = models.IntegerField()
    faixa_etaria_max = models.IntegerField()

    def __str__(self):
        return str(self.modalidade)
"""
