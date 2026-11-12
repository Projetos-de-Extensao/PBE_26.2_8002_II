from django.db import migrations


CAPACIDADES_SALA = {
    "Área de Treinamento Funcional e Gramado Sintético": 20,
    "Laboratório de Avaliação Física": 10,
    "Consultório de Nutrição Esportiva": 4,
    "Espaço de Fisioterapia e Recovery": 4,
}


def atualizar_capacidades(apps, schema_editor):
    sala_model = apps.get_model("app", "Sala")
    for nome, capacidade in CAPACIDADES_SALA.items():
        sala_model.objects.filter(nome=nome).update(capacidade=capacidade)


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_alter_servico_nome"),
    ]

    operations = [
        migrations.RunPython(atualizar_capacidades, migrations.RunPython.noop),
    ]
