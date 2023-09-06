# Generated by Django 4.2.3 on 2023-07-31 20:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeiro', '0007_pessoa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_vencimento', models.DateField(default=datetime.datetime.now)),
                ('data_pagamento', models.DateField(blank=True, default=datetime.datetime.now)),
                ('descricao', models.CharField(max_length=50)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.CharField(choices=[('D', 'Despesa'), ('R', 'Receita'), ('T', 'Transferencia')], default='D', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financeiro.categoria')),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financeiro.conta')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financeiro.pessoa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data_vencimento', 'data_pagamento', 'tipo'],
            },
        ),
    ]
