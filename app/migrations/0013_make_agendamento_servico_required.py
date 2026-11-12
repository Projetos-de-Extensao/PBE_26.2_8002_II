from django.db import migrations, models
import django.db.models.deletion


def preencher_servicos_ausentes(apps, schema_editor):
    agendamento_model = apps.get_model("app", "Agendamento")
    servico_model = apps.get_model("app", "Servico")
    servico_padrao = servico_model.objects.filter(
        nome="Treinamento Funcional"
    ).first()

    if servico_padrao is not None:
        agendamento_model.objects.filter(servico__isnull=True).update(
            servico=servico_padrao
        )


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0012_catalogo_servicos"),
    ]

    operations = [
        migrations.RunPython(
            preencher_servicos_ausentes,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="agendamento",
            name="servico",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="agendamentos",
                to="app.servico",
            ),
        ),
    ]
