# Generated by Django 4.2.3 on 2023-09-20 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0033_alter_tipo_options_remove_tipo_tipo_ordem_tipo_ordem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'ordering': ['ordem', 'nome']},
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='tipo',
        ),
        migrations.AddField(
            model_name='grupo',
            name='ordem',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]