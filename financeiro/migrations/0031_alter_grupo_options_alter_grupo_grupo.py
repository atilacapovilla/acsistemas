# Generated by Django 4.2.3 on 2023-09-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0030_alter_grupo_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'ordering': ['tipo', 'grupo', 'nome']},
        ),
        migrations.AlterField(
            model_name='grupo',
            name='grupo',
            field=models.CharField(choices=[('1RE', 'Receitas'), ('2RD', 'Rendimentos'), ('3DF', 'Despesas Fixas'), ('4DV', 'Despesas Variaveis'), ('5DE', 'Despesas Extras'), ('6DA', 'Despesas Adicionais'), ('7TR', 'Tranferencia')], default='1RE', max_length=3),
        ),
    ]
