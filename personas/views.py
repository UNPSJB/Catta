from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from personas.models import Persona
from personas.forms import CuentaNuevaForm, LoginForm


def index(request):
    return render(request, 'principal/index.html', {})

def login(request):
    return render(request, 'login/login.html', {})

def cuenta(request):
    ret = 'cuentaNueva/cuenta_nueva.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            ret = 'cliente/index_cliente.html'
    else:
        form = CuentaNuevaForm

    return render(request, ret, {"form": form})

def empleado(request):
    ret = 'empleado/index_empleado.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            ret = 'cliente/index_cliente.html'
    else:
        form = CuentaNuevaForm

    return render(request, ret, {"form": form})

def nuevo_empleado(request):
    return render(request, 'empleado/nuevo_empleado.html', {})

def duenio(request):
    ret = 'duenio/index_duenio.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            ret = 'cliente/index_cliente.html'
    else:
        form = CuentaNuevaForm

    return render(request, ret, {"form": form})

def cliente(request):
    return render(request, 'cliente/index_cliente.html', {})

def nuevo_cliente(request):
    return render(request, 'cliente/nuevo_cliente.html', {})

def index_turnos(request):
	return render(request, 'Turnos/index_turnos.html', {})
