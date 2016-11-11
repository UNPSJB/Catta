from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from personas.forms import CuentaNuevaForm, EmpleadoNuevoForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm, PromoForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm, RegistrarTurnoRealizadoForm, EliminarTurnoForm

from personas.models import Persona
from gestion.models import ServicioBasico, Promocion, Insumo, Servicio
from turnos.models import Turno

from django.db.models import Q

"""Metodo de Filtro"""

def get_filtros(modelo, datos):
    filtros = []
    valores = {}
    for key, value in datos.items():
        if value:
            valores[key] = value
            q = Q()
            for mfilter in modelo.FILTROS[key]:
                q |= Q(**{mfilter: value})
            filtros.append(q)
    return (filtros, valores)

"""
Vistas del Cliente.
"""
@login_required(login_url='iniciar_sesion')
def cliente(request):
    promociones = Promocion.objects.all()
    return render(request, 'cliente/index_cliente.html', {'promociones': promociones})


FORMS_EMPLEADO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_crear_turno', 'crear_turno'): CrearTurnoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
    ('form_eliminar_turno', 'eliminar_turno'): EliminarTurnoForm,
    ('form_registrar_turno_realizado', 'registrar_turno_realizado'):RegistrarTurnoRealizadoForm
}


"""
Vistas del Empleado.
"""

def get_filtros(modelo, datos):
    filtros = []
    valores = {}
    for key, value in datos.items():
        if value:
            valores[key] = value
            q = Q()
            for mfilter in modelo.FILTROS[key]:
                q |= Q(**{mfilter: value})
            filtros.append(q)
    return (filtros, valores)



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
            elif input_name == 'registrar_turno_realizado':
                _form = RegistrarTurnoRealizadoForm(instance=turno)
                contexto[form_name] = _form
            elif input_name == 'eliminar_turno':
                _form = EliminarTurnoForm(instance=turno)
                contexto[form_name] = _form
            else:
                contexto[form_name] = klassForm()

    return render(request, ret, contexto)


def empleado_lista_clientes(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    clientes = Persona.objects.filter(cliente__isnull=False, *mfiltros)
    return render(request, 'empleado/clientes_empleado.html', {'clientes': clientes, "f":ffilter})


def empleado_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()
    return render(request, 'duenio/servicios_duenio.html', {'servicios': servicios,
                                                            'promociones': promociones,
                                                            'insumos': insumos, "f": ffilter})


def empleado_lista_insumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'insumo/listaInsumos.html', {'insumos': insumos, "f": ffilter})
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
            _form = klassForm(request.POST or None, request.FILES or None)
            if _form.is_valid():
                _form.save()
                _form = klassForm()
                redirect(usuario.get_vista())
            contexto[form_name] = _form
        else:
            contexto[form_name] = klassForm()

    return render(request, ret, contexto)


def duenio_lista_empleados(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    empleados = Persona.objects.filter(empleado__isnull=False, *mfiltros)
    return render(request, 'duenio/empleados_duenio.html', {'empleados': empleados, "f": ffilter})


def duenio_lista_clientes(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    clientes = Persona.objects.filter(cliente__isnull=False, *mfiltros)
    return render(request, 'duenio/clientes_duenio.html', {'clientes': clientes, "f": ffilter})


def duenio_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()
    return render(request, 'duenio/servicios_duenio.html', {'servicios': servicios,
                                                            'promociones': promociones,
                                                             'insumos': insumos, "f": ffilter})

def duenio_lista_insumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'insumo/listaInsumos.html', {'insumos': insumos, "f": ffilter})

def duenio_lista_turnos(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros).order_by('fecha')
    return render(request, 'duenio/turnos_duenio.html', {'turnos': turnos, "f": ffilter})


def agenda(request):
    return render(request, 'duenio/agenda_duenio.html', {})

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
    ret = 'cuentaNueva/cuenta_nueva.html'

    if request.method == "POST":
        form = CuentaNuevaForm(request.POST)
        if form.is_valid():
            form.save()
            usuario = request.user
            login(request, usuario)

            return redirect(usuario.get_vista())
    else:
        form = CuentaNuevaForm()

    return render(request, ret, {"form": form})


def cerrar_sesion(request):
    logout(request)
    return redirect('index')


