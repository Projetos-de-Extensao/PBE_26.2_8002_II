from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_padronizar_salas"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servico",
            name="nome",
            field=models.CharField(
                choices=[
                    ("Nutrição Esportiva", "nutricao_esportiva"),
                    ("Fisioterapia", "fisioterapia"),
                    ("Recuperação Muscular", "recuperacao_muscular"),
                    ("Preparação Física", "preparacao_fisica"),
                    ("Treinamento Funcional", "treinamento_funcional"),
                    ("Avaliação de Performance", "avaliacao_performance"),
                ],
                default="Nome do serviço",
                unique=True,
            ),
        ),
    ]
