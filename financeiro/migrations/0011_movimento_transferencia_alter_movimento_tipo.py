# Generated by Django 4.2.3 on 2023-08-04 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_alter_movimento_data_pagamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='transferencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movimento',
            name='tipo',
            field=models.CharField(choices=[('D', 'Despesa'), ('R', 'Receita')], default='D', max_length=1),
        ),
    ]
