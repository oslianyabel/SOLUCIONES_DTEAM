# Generated by Django 4.2.3 on 2024-10-04 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_equipo_imagen_dir'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('hero', models.ImageField(upload_to='imagenes/index')),
                ('hero_dir', models.CharField(default='/media/imagenes/index/hero.jpg', max_length=255)),
                ('why_us', models.ImageField(upload_to='imagenes/servicios')),
                ('why_us_dir', models.CharField(default='/media/imagenes/index/why_us.jpg', max_length=255)),
                ('skills', models.ImageField(upload_to='imagenes/servicios')),
                ('skills_dir', models.CharField(default='/media/imagenes/index/skills.jpg', max_length=255)),
                ('action', models.ImageField(upload_to='imagenes/servicios')),
                ('action_dir', models.CharField(default='/media/imagenes/index/action.jpg', max_length=255)),
            ],
        ),
    ]
