from django.contrib import admin

from .models import (
    Agendamento,
    Aluno,
    Ocupacao,
    Profissional,
    RegistroTreinamento,
    Responsavel,
    Sala,
    Servico,
)

# Register your models here.
admin.site.register(Sala)
admin.site.register(Aluno)
admin.site.register(Profissional)
admin.site.register(Responsavel)
admin.site.register(Agendamento)
admin.site.register(Ocupacao)
admin.site.register(RegistroTreinamento)
admin.site.register(Servico)
