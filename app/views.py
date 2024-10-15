from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import *
from core import assistant


def index(request):
    sn = SobreNosotros.objects.filter(activo=True)[0]
    pot = Potencialidad.objects.filter(activo=True)[:3]
    skills = Skill.objects.filter(activo=True)[:4]
    cat = Categoria.objects.filter(activo=True)
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


def servicios(request, category_id):
    try:
        categoria = Categoria.objects.get(id = category_id)
        serv = Servicio.objects.filter(categoria = categoria, activo=True).order_by('imagen')
    except Categoria.DoesNotExist:
        serv = Servicio.objects.filter(activo=True).order_by('imagen')
        
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


def login_opinion(request, service_id):
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
    return render(request, 'accounts/login_opinion.html', context)


def register_opinion(request, service_id):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login_opinion', args=[service_id]))
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
    return render(request, 'accounts/register_opinion.html', context)


def login_chatbot(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('chatbot'))
        # credenciales incorrectas    
        messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    context = {
        "form": form,
    }
    return render(request, 'accounts/login_chatbot.html', context)


def register_chatbot(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login_chatbot'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    context = {
        "form": form,
    }
    return render(request, 'accounts/register_chatbot.html', context)


def opinion(request, service_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login_opinion', args=[service_id]))
    
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


def chatbot(request):
    if request.method == 'POST':
        # se obtiene el nuevo mensaje enviado por el usuario
        msg = request.POST["Body"]
        print(f"- User: {msg}")
        
        if not request.user.is_authenticated:
            print("Usuario no autenticado.")
            ans, ok = assistant.run_conversation(request.user, msg)
            print(f"- Bot: {ans}")
            hora_actual = datetime.now().strftime("%I:%M:%S %p")
            return JsonResponse({'text': ans, "status": "success", "time": hora_actual})
        
        # se busca la conversacion del usuario autenticado
        try:
            conv = Conversacion.objects.get(usuario = request.user)
            print("Conversacion encontrada.")
        except Conversacion.DoesNotExist:
            conv = Conversacion.objects.create(usuario=request.user)
            print("Conversacion creada.")
            
        # se filtran los mensajes de la conversacion
        msg_list_obj = Mensaje.objects.filter(conversacion = conv).order_by('fecha_envio')
        if not msg_list_obj.exists():
            print("No hay mensajes en la conversación.")
            msg += f". Me llamo {request.user}. Refiérete a mí por ese nombre."
            ans, ok = assistant.run_conversation(request.user, msg)
            print(f"- Bot: {ans}")
            if ok:
                sys_prompt = assistant.get_sys_prompt()
                print(sys_prompt)
                Mensaje.objects.create(
                    conversacion=conv,
                    texto=sys_prompt,
                    enviado_por="system"
                )
                Mensaje.objects.create(
                    conversacion=conv,
                    texto=msg,
                    enviado_por="user"
                )
                Mensaje.objects.create(
                    conversacion=conv,
                    texto=ans,
                    enviado_por="assistant"
                )
            hora_actual = datetime.now().strftime("%I:%M:%S %p")
            return JsonResponse({'text': ans, "status": "success", "time": hora_actual})
        
        # se crea un historial de mensajes para el asistente
        history = []
        for msg_obj in msg_list_obj:
            temp = {
                "role": str(msg_obj.enviado_por),
                "content": str(msg_obj.texto),
            }
            history.append(temp)
        
        # se envia el mensaje con el historial al asistente y se obtiene su respuesta
        ans, ok = assistant.run_conversation(request.user, msg, history)
        print(f"- Bot: {ans}")
        
        if ok:
            # Si la respuesta del asistente fue correcta se agregan los mensajes a la conversación.
            Mensaje.objects.create(
                conversacion=conv,
                texto=msg,
                enviado_por="user"
            )
            Mensaje.objects.create(
                conversacion=conv,
                texto=ans,
                enviado_por="assistant"
            )
            
        hora_actual = datetime.now().strftime("%I:%M:%S %p")
        return JsonResponse({'text': ans, "status": "success", "time": hora_actual})
        
    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "catalogo": catalogo,
    }
    return render(request, 'chatbot.html', context)


def chatbot_service(request, service_id):
    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "catalogo": catalogo,
    }
    return render(request, 'chatbot.html', context)


def chatbot_admin(request):
    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "catalogo": catalogo,
    }
    return render(request, 'chatbot.html', context)
