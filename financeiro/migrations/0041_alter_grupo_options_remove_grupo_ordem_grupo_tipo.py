# Generated by Django 4.2.3 on 2023-09-22 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0040_categoria_valor_planejamento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'ordering': ['tipo', 'nome']},
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='ordem',
        ),
        migrations.AddField(
            model_name='grupo',
            name='tipo',
            field=models.CharField(choices=[('E', 'Entrada'), ('S', 'Saida'), ('T', 'Tranferencia')], default='S', max_length=2),
        ),
    ]
