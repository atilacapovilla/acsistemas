# Generated by Django 4.2.3 on 2023-08-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0025_alter_movimento_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('FX', 'Fixa'), ('VR', 'Variavel'), ('TR', 'Tranferencia'), ('RD', 'Rendimentos')], default='VR', max_length=2),
        ),
    ]
