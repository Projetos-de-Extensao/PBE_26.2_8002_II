from django.db import migrations


SERVICOS = {
    "Nutrição Esportiva": "Avaliação corporal e planejamento alimentar para atletas.",
    "Fisioterapia": "Reabilitação e prevenção de lesões esportivas.",
    "Recuperação Muscular": "Protocolos de recuperação muscular após treinos e jogos.",
    "Preparação Física": "Treinos de força, potência, agilidade e condicionamento.",
    "Treinamento Funcional": "Exercícios de coordenação, mobilidade e fundamentos motores.",
    "Avaliação de Performance": "Testes físicos e análise de desempenho esportivo.",
}


def criar_catalogo_servicos(apps, schema_editor):
    servico_model = apps.get_model("app", "Servico")
    for nome, descricao in SERVICOS.items():
        servico, criado = servico_model.objects.get_or_create(
            nome=nome,
            defaults={"descricao": descricao, "duracao_minutos": 30},
        )
        if not criado and not servico.descricao:
            servico.descricao = descricao
            servico.save(update_fields=["descricao"])


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0011_atualizar_capacidades_salas"),
    ]

    operations = [
        migrations.RunPython(criar_catalogo_servicos, migrations.RunPython.noop),
    ]
