from django.shortcuts import render, redirect
from django.contrib.auth import login

from personas.models import Persona

from catta.forms import LoginForm


def index(request):
    return render(request, 'principal/index.html', {})


def iniciar_sesion(request):
    if request.method == "POST":
        form = LoginForm(None, request.POST)
        if form.is_valid():
            usuario = form.user_cache
            login(request, form.get_user())

            p = Persona.objects.filter(usuario=usuario).get()

            if p.duenia is not None:
                return redirect('duenio')
            else:
                if p.empleado is not None:
                    return redirect('empleado')
                else:
                    return redirect('cliente')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})
