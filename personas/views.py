from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from personas.forms import CuentaNuevaForm, EmpleadoNuevoForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm, PromoForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm 

from personas.models import Persona, Cliente, Empleado
from gestion.models import Servicio, Insumo
from turnos.models import Turno


"""
Vistas del Cliente.
"""
@login_required(login_url='iniciar_sesion')
def cliente(request):
    promociones = Servicio.promociones.all()
    return render(request, 'cliente/index_cliente.html', {'promociones': promociones})


FORMS_EMPLEADO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_crear_turno', 'crear_turno'): CrearTurnoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
}

"""
Vistas del Empleado.
"""
@login_required(login_url='iniciar_sesion')
def empleado(request):
    usuario = request.user
    ret = 'empleado/index_empleado.html'
    contexto = {}
    turno = Turno.objects.get(id=1)
    print(turno)
    for form_name, input_name in FORMS_EMPLEADO:
        klassForm = FORMS_EMPLEADO[(form_name, input_name)]
        print('estoy')
        if request.method == "POST" and input_name in request.POST:
            _form = klassForm(request.POST)
            if _form.is_valid:
                _form.save()
                _form = klassForm()
                redirect(usuario.get_vista())
            contexto[form_name] = _form
        else:
            if input_name == 'modificar_turno':
                _form = ModificarTurnoForm(instance=turno)
                contexto[form_name] = _form
            else:
                contexto[form_name] = klassForm()

    return render(request, ret, contexto)

def empleado_lista_clientes(request):
    clientes = Persona.objects.filter(cliente__isnull=False)
    return render(request, 'empleado/clientes_empleado.html', {'clientes': clientes})

def empleado_lista_servicios(request):
    servicios = Servicio.objects.all()
    insumos = Insumo.objects.all()
    return render(request, 'empleado/servicios_empleado.html', {'servicios': servicios,
                                                            'insumos': insumos})

def empleado_lista_insumos(request):
    insumos = Insumo.objects.all()
    return render(request, 'empleado/insumos_empleado.html', {'insumos': insumos})

"""
Vistas de la Dueña
"""
# La clave es el nombre del form, el nombre del input
FORMS_DUENIO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_empleado', 'crear_empleado'): EmpleadoNuevoForm,
    ('form_sector', 'crear_sector'): SectorForm,
    ('form_servicio', 'crear_servicio'): ServicioForm,
    ('form_crear_turno', 'crear_turno'): CrearTurnoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
    ('form_promo', 'crear_promo'): PromoForm,
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


def duenio_lista_empleados(request):
    empleados = Persona.objects.filter(empleado__isnull=False)
    return render(request, 'duenio/empleados_duenio.html', {'empleados': empleados})


def duenio_lista_clientes(request):
    clientes = Persona.objects.filter(cliente__isnull=False)
    return render(request, 'duenio/clientes_duenio.html', {'clientes': clientes})

def duenio_lista_servicios(request):
    servicios = Servicio.objects.all()
    insumos = Insumo.objects.all()
    return render(request, 'duenio/servicios_duenio.html', {'servicios': servicios,
                                                            'insumos': insumos})

def duenio_lista_insumos(request):
    insumos = Insumo.objects.all()
    return render(request, 'duenio/insumos_duenio.html', {'insumos': insumos})

def duenio_lista_turnos(request):
    turnos = Turno.objects.all().order_by('fecha')
    return render(request, 'duenio/turnos_duenio.html', {'turnos': turnos})

# TODO Ver si esto es realmente necesario.
def nuevo_empleado(request):
    return render(request, 'empleado/nuevo_empleado.html', {})


# TODO Ver si esto es realmente necesario.
def index_turnos(request):
    return render(request, 'Turnos/index_turnos.html', {})

"""
Vistas del control de cuentas.
"""
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

def cerrar_sesion(request):
    logout(request)
    return redirect('index')
