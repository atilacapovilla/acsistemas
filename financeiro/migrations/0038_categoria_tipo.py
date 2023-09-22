# Generated by Django 4.2.3 on 2023-09-21 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0037_alter_categoria_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('FX', 'Fixa'), ('VR', 'Variavel'), ('TR', 'Tranferencia'), ('RD', 'Rendimentos')], default='VR', max_length=2),
        ),
    ]
