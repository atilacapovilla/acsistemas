# Generated by Django 4.2.3 on 2023-09-20 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0034_alter_grupo_options_remove_grupo_grupo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='essencial',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='tipo',
        ),
    ]
