from django.db import migrations, models


SALAS_PADRAO = [
    "Área de Treinamento Funcional e Gramado Sintético",
    "Laboratório de Avaliação Física",
    "Consultório de Nutrição Esportiva",
    "Espaço de Fisioterapia e Recovery",
]


def criar_salas_padrao(apps, schema_editor):
    sala_model = apps.get_model("app", "Sala")
    for nome in SALAS_PADRAO:
        sala_model.objects.get_or_create(
            nome=nome,
            defaults={"capacidade": 1, "disponivel": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_alter_servico_nome"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sala",
            name="nome",
            field=models.CharField(
                choices=[(sala, sala) for sala in SALAS_PADRAO],
                max_length=100,
            ),
        ),
        migrations.RunPython(criar_salas_padrao, migrations.RunPython.noop),
    ]
