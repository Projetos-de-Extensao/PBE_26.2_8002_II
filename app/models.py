from django.db import models

class Sala(models.Model):
    id = models.TextField().primary_key
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    disponivel = models.BooleanField()

    def __str__(self):
        return self.nome
