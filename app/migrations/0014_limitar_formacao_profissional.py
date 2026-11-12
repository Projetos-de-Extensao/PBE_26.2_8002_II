from django.db import migrations, models


TIPOS_SERVICO = [
    ("Nutrição Esportiva", "nutricao_esportiva"),
    ("Fisioterapia", "fisioterapia"),
    ("Recuperação Muscular", "recuperacao_muscular"),
    ("Preparação Física", "preparacao_fisica"),
    ("Treinamento Funcional", "treinamento_funcional"),
    ("Avaliação de Performance", "avaliacao_performance"),
]


def normalizar_formacoes_conhecidas(apps, schema_editor):
    profissional_model = apps.get_model("app", "Profissional")
    profissional_model.objects.filter(ocupacao="Fisioterapeuta").update(
        ocupacao="Fisioterapia"
    )
    profissional_model.objects.filter(ocupacao="Preparador físico").update(
        ocupacao="Preparação Física"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0013_make_agendamento_servico_required"),
    ]

    operations = [
        migrations.RunPython(
            normalizar_formacoes_conhecidas,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="profissional",
            name="ocupacao",
            field=models.CharField(
                choices=TIPOS_SERVICO,
                max_length=100,
            ),
        ),
    ]
