from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
import datetime

from personas.models import Persona
from gestion.models import ServicioBasico, Promocion

from catta.forms import LoginForm

def index(request):
    contexto = {}
    contexto["promociones"] = Promocion.objects.all()
    contexto["logeado"] = True
    try:
        persona = request.user.persona
        rol = persona.get_rol_url()
        contexto['rol'] = rol
    except AttributeError:
        contexto["logeado"] = False
    return render(request, 'principal/index.html', contexto)

def iniciar_sesion(request):
    if request.method == "POST":
        form = LoginForm(None, request.POST)
        if form.is_valid():
            usuario = form.user_cache
            login(request, form.get_user())
            return redirect(usuario.get_vista())
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})
