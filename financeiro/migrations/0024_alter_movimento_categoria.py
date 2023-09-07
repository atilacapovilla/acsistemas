# Generated by Django 4.2.3 on 2023-08-16 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0023_categoria_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimento',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='financeiro.categoria'),
        ),
    ]