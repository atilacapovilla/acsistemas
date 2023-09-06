# Generated by Django 4.2.3 on 2023-08-07 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0015_conta_saldo_inicial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimento',
            name='transferencia',
        ),
        migrations.AlterField(
            model_name='contasaldo',
            name='conta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeiro.conta'),
        ),
    ]
