# Generated by Django 4.2.3 on 2024-01-16 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeiro', '0044_remove_grupo_usuario_alter_grupo_nome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
