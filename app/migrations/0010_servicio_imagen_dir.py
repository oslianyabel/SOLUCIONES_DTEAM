# Generated by Django 4.2.16 on 2024-10-03 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_equipo_fuente_alter_equipo_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='imagen_dir',
            field=models.CharField(default='imagenes/servicios/nombre.jpg', max_length=255),
        ),
    ]
