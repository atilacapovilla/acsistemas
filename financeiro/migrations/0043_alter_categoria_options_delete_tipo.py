# Generated by Django 4.2.3 on 2023-10-09 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0042_alter_grupo_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'ordering': ['nome']},
        ),
        migrations.DeleteModel(
            name='Tipo',
        ),
    ]
