# Generated by Django 5.1.1 on 2024-10-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_servicio_puntos_promedio_servicio_votos_comentario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='aprobado',
            field=models.BooleanField(default=False),
        ),
    ]
