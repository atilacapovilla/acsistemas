# Generated by Django 4.2.3 on 2023-08-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0009_alter_movimento_data_pagamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimento',
            name='data_pagamento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movimento',
            name='data_vencimento',
            field=models.DateField(),
        ),
    ]
