from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

from .forms import CuentaNuevaForm, EmpleadoNuevoForm, LiquidarComisionForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm, PromoForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm, RegistrarTurnoRealizadoForm, EliminarTurnoForm, CrearTurnoFijoForm

from .models import Persona, Empleado
from gestion.models import ServicioBasico, Promocion, Insumo, Servicio
from turnos.models import Turno, TurnoFijo
from django.db.models import Q, Count
from datetime import datetime

"""Metodo de Filtro"""
def get_filtros(modelo, datos):
    filtros = []
    valores = {}
    for key, value in datos.items():
        if value:
            valores[key] = value
            q = Q()
            if type(modelo.FILTROS[key]) == dict:
                q |= modelo.FILTROS[key][int(value)]
            else:
                for mfilter in modelo.FILTROS[key]:
                    q |= Q(**{mfilter: value})
            filtros.append(q)
    return (filtros, valores)

"""
Vistas del Cliente.
"""
FORMS_CLIENTE = {
    ('form_crear_turno_cliente', 'crear_turno_cliente'): CrearTurnoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
    ('form_eliminar_turno', 'eliminar_turno'): EliminarTurnoForm,

}
@login_required(login_url='iniciar_sesion')
#@permission_required('personas.cliente_puede_ver', raise_exception=True)
def cliente(request):

    promociones = Promocion.objects.all()
    # return render(request, 'cliente/index_cliente.html', {'promociones': promociones})

    usuario = request.user
    ret = 'cliente/index_cliente.html'
    contexto = {}
    turno = Turno.objects.get(id=1)
    for form_name, input_name in FORMS_CLIENTE:
        klassForm = FORMS_CLIENTE[(form_name, input_name)]
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
            elif input_name == 'eliminar_turno':
                _form = EliminarTurnoForm(instance=turno)
                contexto[form_name] = _form
            else:
                contexto[form_name] = klassForm()
    contexto = {'promociones': promociones}

    return render(request, ret, contexto)


def crear_turno_cliente(request):
    if request.method == "POST":
        form = CrearTurnoForm(request.POST)
        if form.is_valid():
            print(request.user.persona.cliente)
            form.save()
            return redirect('/personas/cliente')
        print(form)
    else:
        form = CrearTurnoForm(initial={'cliente': request.user.persona.cliente})
        form.fields['cliente'].widget = forms.HiddenInput()
    return render(request, 'cliente/crear_turno.html', {"form": form})


def agenda_cliente(request):
    return render(request, 'cliente/agenda_cliente.html', {})


def cliente_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()
    return render(request, 'cliente/servicios_cliente.html', {'servicios': servicios,
                                                              'promociones': promociones,
                                                              'insumos': insumos, "f": ffilter})


def cliente_lista_turnos(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    usuario = request.user
    turnos = Turno.objects.filter(cliente__persona__dni__exact=usuario.persona.dni, *mfiltros).order_by('-fecha')
    return render(request, 'cliente/turnos_cliente.html', {'turnos': turnos, "f": ffilter})



FORMS_EMPLEADO = {
    ('form_cliente', 'crear_cuenta'): CuentaNuevaForm,
    ('form_crear_turno', 'crear_turno'): CrearTurnoForm,
    ('form_servicio', 'crear_servicio'): ServicioForm,
    ('form_promo', 'crear_promo'): PromoForm,
    ('form_modificar_turno', 'modificar_turno'): ModificarTurnoForm,
    ('form_eliminar_turno', 'eliminar_turno'): EliminarTurnoForm,
    ('form_registrar_turno_realizado', 'registrar_turno_realizado'): RegistrarTurnoRealizadoForm,
    ('form_crear_turno_fijo', 'crear_turno_fijo'): CrearTurnoFijoForm,
    ('form_servicio', 'crear_servicio'): ServicioForm,
    ('form_promo', 'crear_promo'): PromoForm
}

"""
Vistas del Empleado.
"""



@login_required(login_url='iniciar_sesion')
@permission_required('personas.empleado_puede_ver', raise_exception=True)
def empleado(request, id=None):
    usuario = request.user
    ret = 'empleado/index_empleado.html'
    contexto = {}
    instance = id and get_object_or_404(Turno, id=id)
    for form_name, input_name in FORMS_EMPLEADO:
        klassForm = FORMS_EMPLEADO[(form_name, input_name)]
        if request.method == "POST" and input_name in request.POST:
            _form = klassForm(request.POST, instance=instance)
            if _form.is_valid:
                _form.save(usuario)
                _form = klassForm()
                redirect(usuario.get_vista())
            contexto[form_name] = _form
        else:
            if input_name == 'modificar_turno':
                _form = ModificarTurnoForm(instance=instance)
                contexto[form_name] = _form
            elif input_name == 'registrar_turno_realizado':
                _form = RegistrarTurnoRealizadoForm(instance=instance)
                contexto[form_name] = _form
            elif input_name == 'eliminar_turno':
                _form = EliminarTurnoForm(instance=instance)
                contexto[form_name] = _form
            else:
                contexto[form_name] = klassForm()

    return render(request, ret, contexto)


def empleado_lista_clientes(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    clientes = Persona.objects.filter(cliente__isnull=False, *mfiltros)
    return render(request, 'empleado/clientes_empleado.html', {'clientes': clientes, "f":ffilter})


def agenda_empleado(request):
    return render(request, 'empleado/agenda_empleado.html', {})


def empleado_lista_turnos(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    usuario = request.user
    turnos = Turno.objects.filter(empleado__persona__dni__exact=usuario.persona.dni, *mfiltros).order_by('-fecha')
    return render(request, 'empleado/turnos_empleado.html', {'turnos': turnos, "f": ffilter, 'Turno':Turno})


def empleado_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()
    return render(request, 'empleado/servicios_empleado.html', {'servicios': servicios,
                                                            'promociones': promociones,
                                                            'insumos': insumos, "f": ffilter})


def empleado_lista_insumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'empleado/insumos_empleado.html', {'insumos': insumos, "f": ffilter})
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
    ('form_registrar_turno_realizado', 'registrar_turno_realizado'): RegistrarTurnoRealizadoForm,
    ('form_promo', 'crear_promo'): PromoForm,
    ('form_insumo', 'crear_insumo'): InsumoForm,
    ('form_liquidar_Comision', 'liquidar_comision'): LiquidarComisionForm,
    ('form_insumo', 'crear_insumo'): InsumoForm,
    ('form_crear_turno_fijo', 'crear_turno_fijo'): CrearTurnoFijoForm
}


@login_required(login_url='iniciar_sesion')
#@permission_required('personas.duenia_puede_ver', raise_exception=True)
def duenio(request):
    usuario = request.user
    ret = 'duenio/index_duenio.html'
    contexto = {}
    if request.method == "POST" and 'liquidar_comision' in request.POST:
        _form = LiquidarComisionForm()
        contexto['form_liquidar_Comision'] = _form
        _fecha = (request.POST.get('fecha'))
        _fecha1 = (request.POST.get('fecha'))
        _fecha += ' 00:00:00'
        _fecha1 += ' 19:45:00'
        id_empleado = (request.POST.get('empleado'))
        _empleado = Empleado.objects.filter(id=id_empleado).first()
        _turnos = Turno.objects.filter(empleado=_empleado, fecha__range=[_fecha, _fecha1])
        _costo = 0
        for turno in _turnos:
            _costo += turno.get_costo()

        _pago = _empleado.get_pago(_costo)

        print(_pago)

    for form_name, input_name in FORMS_DUENIO:
        klassForm = FORMS_DUENIO[(form_name, input_name)]
        if request.method == "POST" and input_name in request.POST and form_name != "form_liquidar_Comision":
            _form = klassForm(request.POST or None, request.FILES or None)
            if _form.is_valid():
                _form.save()
                _form = klassForm()
                redirect(usuario.get_vista())
            contexto[form_name] = _form
        else:
            contexto[form_name] = klassForm()

    #_turno = TurnoFijo.objects.latest('id')
    #t= TurnoFijo.objects.last()
    print(_turno)
    return render(request, ret, contexto)


def duenio_lista_empleados(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    empleados = Persona.objects.filter(empleado__isnull=False, *mfiltros)
    return render(request, 'empleado/listaEmpleados.html', {'empleados': empleados, "f": ffilter})


def modificarComision(request, id):
    persona = get_object_or_404(Persona, pk=id)
    if request.method == "POST":
        persona.empleado.porc_comision = request.POST['NuevaComision']
        persona.empleado.save()
        return redirect('/personas/duenio_lista_empleados')
    else:
        persona = get_object_or_404(Persona, pk=id)
    return render(request, 'empleado/modificarComision.html', {'persona': persona})


def duenio_lista_clientes(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    clientes = Persona.objects.filter(cliente__isnull=False, *mfiltros)
    return render(request, 'duenio/clientes_duenio.html', {'clientes': clientes, "f": ffilter})


def duenio_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()

    topServicios = ServicioBasico.objects.annotate(cantidad_de_turnos=Count("turnos")).order_by("-cantidad_de_turnos")[:5]

    return render(request, 'duenio/servicios_duenio.html', {'servicios': servicios,
                                                            'promociones': promociones,
                                                             'insumos': insumos,
                                                            'topServicios': topServicios,
                                                            "f": ffilter})


def modificar_stock_duenio(request, id):
    insumo = get_object_or_404(Insumo, pk=id)
    if request.method == "POST":
        insumo.stock = request.POST['stockNuevo']
        insumo.save()
        return redirect('/personas/duenio_lista_insumos')
    else:
        insumo = get_object_or_404(Insumo, pk=id)
    return render(request, 'duenio/modificar_stock_duenio.html', {'insumo': insumo})


def duenio_lista_insumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'duenio/insumos_duenio.html', {'insumos': insumos, "f": ffilter})


def duenio_lista_turnos(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros).order_by('-fecha')
    return render(request, 'duenio/turnos_duenio.html', {'turnos': turnos, "f": ffilter, 'Turno':Turno})


def agenda_duenio(request):
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
            usuario = form.save()
            login(request, usuario)

            return redirect(usuario.get_vista())
    else:
        form = CuentaNuevaForm()

    return render(request, ret, {"form": form})


def cerrar_sesion(request):
    logout(request)
    return redirect('index')
