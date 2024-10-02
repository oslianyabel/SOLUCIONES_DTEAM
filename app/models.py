from django.db import models

class SobreNosotros(models.Model):
    parrafo = models.TextField(null=False)
    documento = models.FileField(upload_to='documentos')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return "Sobre nosotros"


class Potencialidad(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.TextField(null=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Skill(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    porcentaje = models.IntegerField(null=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    abreviatura = models.CharField(max_length=255, null=False)
    descripcion = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.TextField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/servicios', null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    imagen = models.ImageField(upload_to='imagenes/equipo')
    nombre = models.CharField(max_length=255, null=False)
    apellido = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    evento = models.CharField(max_length=255)
    fecha = models.DateField()
    fuente = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class PreguntaFrecuente(models.Model):
    pregunta = models.CharField(max_length=255, null=False)
    respuesta = models.TextField(null=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.pregunta
    

class Link(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    link = models.URLField(null=False)

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
        return "Contacto"


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
  