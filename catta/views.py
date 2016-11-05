from django.shortcuts import render, redirect
from django.contrib.auth import login

from personas.models import Persona
from gestion.models import ServicioBasico, Promocion

from catta.forms import LoginForm


def index(request):
    promociones = Promocion.objects.all()
    return render(request, 'principal/index.html', {'promociones': promociones})


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
