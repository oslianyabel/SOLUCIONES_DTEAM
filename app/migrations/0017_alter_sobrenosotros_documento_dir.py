# Generated by Django 4.2.3 on 2024-10-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_sobrenosotros_documento_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sobrenosotros',
            name='documento_dir',
            field=models.CharField(default='/media/documentos/datos.doc', max_length=255),
        ),
    ]
