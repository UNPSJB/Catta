from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from personas.forms import CuentaNuevaForm, EmpleadoNuevoForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm
from turnos.forms import TurnoForm


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
        form_clientes = CuentaNuevaForm(request.POST)
        form_turnos = TurnoForm(request.POST)

        if 'crear_cuenta' in request.POST:
            if form_clientes.is_valid():
                form_clientes.save()
                return redirect('empleado')
        elif 'crear_turno' in request.POST:
            if form_turnos.is_valid():
                form_turnos.save()
                return redirect('empleado')

    else:
            form_clientes = CuentaNuevaForm()
            form_turnos = TurnoForm()

    return render(request, ret,  {'form_clientes' : form_clientes ,
                       'form_turnos' : form_turnos})


# La clave es el nombre del form, el nombre del input
FORMS_DUENIO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_empleado', 'crear_emplado'): EmpleadoNuevoForm,
    ('form_sector', 'crear_sector'): SectorForm,
    ('form_servicio', 'crear_servicio'): ServicioForm,
    ('form_turno', 'crear_turno'): TurnoForm,
    ('form_insumo', 'crear_insumo'): InsumoForm
}

@login_required(login_url='iniciar_sesion')
def duenio(request):
    usuario = request.user

    contexto = {}
    for form_name, input_name in FORMS_DUENIO:
        klassForm = FORMS_DUENIO[(form_name, input_name)]
        if request.method == "POST" and input_name in request.POST:
            _form = klassForm(request.POST)
            if _form.is_valid():
                _form.save()
                _form = klassForm()
                redirect(usuario.get_vista())
            contexto[form_name] = _form
        else:
            contexto[form_name] = klassForm()

    return render(request, 'duenio/index_duenio.html', contexto)


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
