from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from personas.forms import CuentaNuevaForm


def index(request):
    return render(request, 'principal/index.html', {})

def login(request):
    return render(request, 'login/login.html', {})

def cuenta(request):
    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            # hacer algo aca con los datos de la form
            print ("asd")
    else:
        form = CuentaNuevaForm
    return render(request, 'cuentaNueva/cuenta_nueva.html', {"form": form})

def empleado(request):
    return render(request, 'empleado/index_empleado.html', {})

def nuevo_empleado(request):
    return render(request, 'empleado/nuevo_empleado.html', {})

def duenio(request):
    return render(request, 'duenio/index_duenio.html', {})

def cliente(request):
    return render(request, 'cliente/index_cliente.html', {})

def nuevo_cliente(request):
    return render(request, 'cliente/nuevo_cliente.html', {})

def index_turnos(request):
	return render(request, 'Turnos/index_turnos.html', {})
