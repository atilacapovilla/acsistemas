# Generated by Django 4.2.3 on 2023-08-04 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0012_contasaldo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conta',
            name='saldo_atual',
        ),
        migrations.RemoveField(
            model_name='conta',
            name='saldo_inicial',
        ),
    ]
