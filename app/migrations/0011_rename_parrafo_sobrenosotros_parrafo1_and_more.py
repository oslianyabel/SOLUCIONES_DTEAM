# Generated by Django 4.2.16 on 2024-10-03 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_servicio_imagen_dir'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sobrenosotros',
            old_name='parrafo',
            new_name='parrafo1',
        ),
        migrations.AddField(
            model_name='sobrenosotros',
            name='check1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sobrenosotros',
            name='check2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sobrenosotros',
            name='check3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sobrenosotros',
            name='parrafo2',
            field=models.TextField(blank=True, null=True),
        ),
    ]
