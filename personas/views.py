from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from personas.forms import CuentaNuevaForm, EmpleadoNuevoForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm


def cuenta(request):
    usuario = request.user
    ret = 'cuentaNueva/cuenta_nueva.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(usuario.get_vista())
    else:
        form = CuentaNuevaForm()

    return render(request, ret, {"form": form})

FORMS_EMPLEADO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_crear_turno', 'crear_turno'): CrearTurnoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
}
def empleado(request):
    usuario = request.user
    ret = 'empleado/index_empleado.html'
    contexto = {}
    for form_name, input_name in FORMS_EMPLEADO:
        klassForm = FORMS_EMPLEADO[(form_name, input_name)]
        if request.method == "POST" and input_name in request.POST:
            _form = klassForm(request.POST)
            if _form.is_valid:
                _form.save()
                _form = klassForm()
                redirect(usuario.get_vista())
            contexto[form_name] = _form
        else:
            contexto[form_name] = klassForm()

    return render(request, ret, contexto)


# La clave es el nombre del form, el nombre del input
FORMS_DUENIO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_empleado', 'crear_emplado'): EmpleadoNuevoForm,
    ('form_sector', 'crear_sector'): SectorForm,
    ('form_servicio', 'crear_servicio'): ServicioForm,
    ('form_crear_turno', 'crear_turno'): CrearTurnoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
    ('form_insumo', 'crear_insumo'): InsumoForm
}

@login_required(login_url='iniciar_sesion')
def duenio(request):
    usuario = request.user
    ret = 'duenio/index_duenio.html'
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

    return render(request, ret, contexto)


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
