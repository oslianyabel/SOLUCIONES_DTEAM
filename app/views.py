from django.shortcuts import render
from .models import *

def index(request):
    sn = SobreNosotros.objects.filter(activo=True)[0]
    pot = Potencialidad.objects.filter(activo=True)[:3]
    skills = Skill.objects.filter(activo=True)[:4]
    cat = Categoria.objects.filter(activo=True)[:3]
    all = Servicio.objects.all()
    ej = [servicio for servicio in all if servicio.imagen and servicio.imagen.url != 'imagenes/servicios/nombre.jpg'][:9]
    team = Equipo.objects.filter(activo=True)[:4]
    preguntas = PreguntaFrecuente.objects.filter(activo=True)[:9]
    contacto = Contacto.objects.filter(activo=True)[0]
    catalogo = Catalogo.objects.filter(activo=True)[0]
    
    context = {
        'sobre_nosotros': sn,
        'potencialidades': pot,
        'skills': skills,
        'categorias': cat,
        'ejemplos': ej,
        'team': team,
        'preguntas': preguntas,
        'contacto': contacto,
        'catalogo': catalogo
    }
    
    return render(request, 'index.html', context)


def servicios(request, cat):
    if cat > 3 or cat < 1:
        serv = Servicio.objects.all().order_by('imagen')
    else:
        serv = Servicio.objects.filter(categoria = cat).order_by('imagen')
    
    catalogo = Catalogo.objects.filter(activo=True)[0]
    contacto = Contacto.objects.filter(activo=True)[0]
    context = {
        "servicios": serv,
        "contacto": contacto,
        "catalogo": catalogo
    }
    return render(request, "servicios.html", context)
