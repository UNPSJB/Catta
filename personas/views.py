from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from personas.forms import CuentaNuevaForm, EmpleadoNuevoForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm


def cuenta(request):
    ret = 'cuentaNueva/cuenta_nueva.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("iniciar_sesion")
    else:
        form = CuentaNuevaForm()

    return render(request, ret, {"form": form})


def empleado(request):
    ret = 'empleado/index_empleado.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            ret = 'cliente/index_cliente.html'
    else:
        form = CuentaNuevaForm()

    return render(request, ret, {"form": form})


@login_required(login_url='iniciar_sesion')
def duenio(request):
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        if request.method == "POST":
            form_clientes = CuentaNuevaForm(request.POST)
            form_empleados = EmpleadoNuevoForm(request.POST)
            form_sector = SectorForm(request.POST)
            form_insumo = InsumoForm(request.POST)
            form_servicio = ServicioForm(request.POST)

            if 'crear_cuenta' in request.POST:
                if form_clientes.is_valid():
                    form_clientes.save()
                    return redirect('duenio')
            elif 'crear_empleado' in request.POST:
                if form_empleados.is_valid():
                    print("antes")
                    form_empleados.save()
                    print("despues")
                    return redirect('duenio')
            elif 'crear_sector' in request.POST:
                if form_sector.is_valid():
                    form_sector.save()
                    return redirect('duenio')
            elif 'crear_insumo' in request.POST:
                if form_insumo.is_valid():
                    form_insumo.save()
                    return redirect('duenio')
            elif 'crear_servicio' in request.POST:
                if form_servicio.is_valid():
                    form_servicio.save()
                    return redirect('duenio')
        else:
            form_clientes = CuentaNuevaForm()
            form_empleados = EmpleadoNuevoForm()
            form_sector = SectorForm()
            form_insumo = InsumoForm()
            form_servicio = ServicioForm()

        return render(request, 'duenio/index_duenio.html',
                      {'form_clientes' : form_clientes ,
                       'form_empleados' : form_empleados ,
                       'form_sector' : form_sector,
                       'form_insumo' : form_insumo,
                       'form_servicio' : form_servicio })


def cliente(request):
    return render(request, 'cliente/index_cliente.html', {})


def nuevo_empleado(request):
    return render(request, 'empleado/nuevo_empleado.html', {})


def nuevo_cliente(request):
    return render(request, 'cliente/nuevo_cliente.html', {})


def index_turnos(request):
    return render(request, 'Turnos/index_turnos.html', {})


def cerrar_sesion(request):
    logout(request)
    return redirect('index')
