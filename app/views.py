from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from .forms import *
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
        serv = Servicio.objects.filter(activo=True).order_by('imagen')
    else:
        serv = Servicio.objects.filter(categoria = cat, activo=True).order_by('imagen')
    
    catalogo = Catalogo.objects.filter(activo=True)[0]
    contacto = Contacto.objects.filter(activo=True)[0]
    context = {
        "servicios": serv,
        "contacto": contacto,
        "catalogo": catalogo
    }
    return render(request, "servicios.html", context)


def servicio_detail(request, service_id):
    try:
        serv = Servicio.objects.get(id = service_id)
        if not serv.activo:
            print(f"El servicio con id: {service_id} no está activo.")
            raise Http404(f"El servicio con id: {service_id} no está activo.")
    except Servicio.DoesNotExist:
        print(f"No hay ningún servicio con id: {service_id}")
        raise Http404(f"No hay ningún servicio con id: {service_id}")
        
    contacto = Contacto.objects.filter(activo=True)[0]
    comentarios = Comentario.objects.filter(servicio = serv, aprobado = True)[:10]
    context = {
        "servicio": serv,
        "comentarios": comentarios,
        "contacto": contacto
    }
    return render(request, "servicio-detail.html", context)


def login_view(request, service_id):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('opinion', args=[service_id]))
        # credenciales incorrectas    
        messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    context = {
        "form": form,
        "service_id": service_id
    }
    return render(request, 'accounts/login.html', context)


def register_view(request, service_id):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login_view', args=[service_id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    context = {
        "form": form,
        "service_id": service_id
    }
    return render(request, 'accounts/register.html', context)


def opinion(request, service_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login_view', args=[service_id]))
    
    contacto = Contacto.objects.filter(activo=True)[0]
    servicio = Servicio.objects.get(id = service_id)
    if not servicio.activo:
        print(f"El servicio con id: {service_id} no está activo.")
        raise Http404(f"El servicio con id: {service_id} no está activo.")
    
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data['comentario']
            puntuacion = int(form.cleaned_data['puntuacion'])
            if comentario != "":
                Comentario.objects.create(
                    usuario=request.user,
                    texto=comentario,
                    servicio=servicio
                )

            total_votos = servicio.votos + 1
            total_puntos = servicio.puntos_promedio * servicio.votos + puntuacion
            servicio.puntos_promedio = total_puntos / total_votos
            servicio.votos = total_votos
            servicio.save()
            return redirect(reverse('servicio-detail', args=[service_id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
    context = {
        "service_id": service_id,
        "servicio": servicio,
        "contacto": contacto,
        'range_1_5': range(1, 6)
    }
    return render(request, 'opinion.html', context)
