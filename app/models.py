from django.db import models

class SobreNosotros(models.Model):
    parrafo = models.TextField()
    parrafo2 = models.TextField(null=True, blank=True)
    check1 = models.CharField(max_length=255, null=True, blank=True)
    check2 = models.CharField(max_length=255, null=True, blank=True)
    check3 = models.CharField(max_length=255, null=True, blank=True)
    documento = models.FileField(upload_to='documentos')
    documento_dir = models.CharField(max_length=255, default='/media/documentos/datos.doc')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.parrafo[:50]


class Potencialidad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Skill(models.Model):
    nombre = models.CharField(max_length=255)
    porcentaje = models.IntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    abreviatura = models.CharField(max_length=255)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    clase = models.CharField(max_length=255, default='fas fa-cloud')
    
    def __str__(self):
        return self.nombre
    
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/servicios', null=True, blank=True)
    imagen_dir = models.CharField(max_length=255, default='media/imagenes/servicios/nombre.jpg')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    imagen = models.ImageField(upload_to='imagenes/equipo')
    imagen_dir = models.CharField(max_length=255, default='/media/imagenes/equipo/nombre.jpg')
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    evento = models.CharField(max_length=255)
    fecha = models.DateField()
    link = models.URLField(max_length=200, null=True, blank=True)
    fuente = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre}"


class PreguntaFrecuente(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.pregunta
    

class Link(models.Model):
    nombre = models.CharField(max_length=255)
    link = models.URLField()
    clase = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre
    

class Contacto(models.Model):
    direccion = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono_fijo = models.CharField(max_length=20)
    telefono_movil = models.CharField(max_length=20)
    links_de_ayuda = models.ManyToManyField(Link, related_name='ayuda')
    redes_sociales = models.ManyToManyField(Link, related_name='redes')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.correo


class Conversacion(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Conversación con {self.usuario.username}'


class Mensaje(models.Model):
    ENVIADO_POR_CHOICES = [
        ('usuario', 'Usuario'),
        ('bot', 'Bot'),
    ]
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    texto = models.TextField()
    enviado_por = models.CharField(max_length=255, choices=ENVIADO_POR_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.enviado_por} en conversación {self.conversacion.id}'


class Catalogo(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    
    hero = models.ImageField(upload_to='imagenes/index')
    hero_dir = models.CharField(max_length=255, default='/media/imagenes/index/hero.jpg')
    
    why_us = models.ImageField(upload_to='imagenes/index')
    why_us_dir = models.CharField(max_length=255, default='/media/imagenes/index/why_us.jpg')
    
    skills = models.ImageField(upload_to='imagenes/index')
    skills_dir = models.CharField(max_length=255, default='/media/imagenes/index/skills.jpg')
    
    action = models.ImageField(upload_to='imagenes/index')
    action_dir = models.CharField(max_length=255, default='/media/imagenes/index/action.jpg')
    
    def __str__(self):
        return self.nombre
  