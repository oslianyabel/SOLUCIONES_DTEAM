# Generated by Django 4.2.3 on 2024-10-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_herramienta_potencialidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='imagen',
            field=models.ImageField(null=True, upload_to='imagenes/servicios'),
        ),
    ]
