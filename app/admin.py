from django.contrib import admin

from .models import (
    Agendamento,
    Aluno,
    # Ocupacao,
    Profissional,
    RegistroTreinamento,
    Responsavel,
    Sala,
    Servico,
)


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "telefone")
    search_fields = ("nome", "cpf", "telefone")
    ordering = ["nome"]
    fieldsets = (
        ("Informações Pessoais", {"fields": ("nome", "cpf", "telefone")}),
        (
            "Autenticação e Acesso",
            {"fields": ("profile",)},
        ),
    )


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "responsavel")
    list_filter = ("responsavel",)
    search_fields = ("nome", "matricula", "responsavel__nome")
    ordering = ["nome"]

    fieldsets = (
        (
            "Dados do Aluno",
            {
                "fields": (
                    "nome",
                    "matricula",
                    "data_nascimento",
                )
            },
        ),
        ("Vínculo Familiar", {"fields": ("responsavel",)}),
    )


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo_profissional", "ocupacao")
    list_filter = ("ocupacao",)
    search_fields = ("nome", "codigo_profissional")
    ordering = ["nome"]

    fieldsets = (
        ("Informações Pessoais", {"fields": ("nome", "codigo_profissional")}),
        ("Atuação na Academia", {"fields": ("ocupacao",)}),
    )


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("nome", "capacidade")
    list_filter = ("capacidade",)
    search_fields = ("nome",)
    ordering = ["nome"]
    fieldsets = (("Configuração da Sala", {"fields": ("nome", "capacidade")}),)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "profissional", "sala", "data_hora", "status")
    list_filter = ("status", "sala", "data_hora", "profissional")
    search_fields = (
        "aluno__nome",
        "aluno__matricula",
        "profissional__codigo_profissional",
    )
    ordering = ["-data_hora"]
    readonly_fields = ("criado_em",)
    fieldsets = (
        ("Participantes e Local", {"fields": ("aluno", "profissional", "sala")}),
        ("Detalhes do Evento", {"fields": ("data_hora", "status")}),
        (
            "Controle do Sistema",
            {
                "fields": ("criado_em",),
                "classes": ("collapse",),
            },
        ),
    )


admin.register(RegistroTreinamento)


class RegistroTreinamentoAdmin(admin.ModelAdmin):
    list_display = ("agendamento", "profissional", "presenca")

    list_filter = ("presenca", "profissional")

    search_fields = ("agendamento__aluno__nome", "profissional__nome")

    fieldsets = (
        ("Vínculo do Treino", {"fields": ("agendamento", "profissional")}),
        ("Status", {"fields": ("presenca",)}),
        (
            "Avaliações e Parecer Técnico",
            {"fields": ("observacoes", "avaliacao_fisica", "avaliacao_tecnica")},
        ),
    )
