from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django import forms

from .forms import CuentaNuevaForm, EmpleadoNuevoForm, LiquidarComisionForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm, PromoForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm, RegistrarTurnoRealizadoForm, EliminarTurnoForm, CrearTurnoFijoForm

from .models import Persona, Empleado, Comision
from gestion.models import ServicioBasico, Promocion, Insumo, Servicio
from turnos.models import Turno, TurnoFijo
from django.db.models import Q, Count
from datetime import datetime, date, time, timedelta



def es_duenio(usuario):
    return usuario.persona.duenia != None

def es_empleado(usuario):
    return usuario.persona.empleado != None

def es_cliente(usuario):
    return usuario.persona.cliente != None


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
@user_passes_test(es_cliente, login_url='restringido', redirect_field_name=None)
def cliente(request):

    promociones = Promocion.objects.all()
    # return render(request, 'cliente/index_cliente.html', {'promociones': promociones})

    ret = 'cliente/index_cliente.html'

    contexto = {'promociones': promociones}

    return render(request, ret, contexto)

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_cliente, login_url='restringido', redirect_field_name=None)
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

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_cliente, login_url='restringido', redirect_field_name=None)
def agenda_cliente(request):
    return render(request, 'cliente/agenda_cliente.html', {})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_cliente, login_url='restringido', redirect_field_name=None)
def cliente_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()
    return render(request, 'cliente/servicios_cliente.html', {'servicios': servicios,
                                                              'promociones': promociones,
                                                              'insumos': insumos, "f": ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_cliente, login_url='restringido', redirect_field_name=None)
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
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
def empleado(request, id=None):
    usuario = request.user
    ret = 'empleado/index_empleado.html'
    contexto = {}
    instance = id and get_object_or_404(Turno, id=id)
    for form_name, input_name in FORMS_EMPLEADO:
        klassForm = FORMS_EMPLEADO[(form_name, input_name)]
        if request.method == "POST" and input_name in request.POST:
            _form = klassForm(request.POST, instance=instance)
            if _form.is_valid():
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

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
def empleado_lista_clientes(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    clientes = Persona.objects.filter(cliente__isnull=False, *mfiltros)
    return render(request, 'empleado/clientes_empleado.html', {'clientes': clientes, "f":ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
def agenda_empleado(request):
    return render(request, 'empleado/agenda_empleado.html', {})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
def empleado_lista_turnos(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    usuario = request.user
    turnos = Turno.objects.filter(empleado__persona__dni__exact=usuario.persona.dni, *mfiltros).order_by('-fecha')
    return render(request, 'empleado/turnos_empleado.html', {'turnos': turnos, "f": ffilter, 'Turno':Turno})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
def empleado_lista_servicios(request):
    mfiltros, ffilter = get_filtros(Servicio, request.GET)
    servicios = ServicioBasico.objects.filter(*mfiltros)
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()
    return render(request, 'empleado/servicios_empleado.html', {'servicios': servicios,
                                                            'promociones': promociones,
                                                            'insumos': insumos, "f": ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
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

#@permission_required('personas.puede_ver_duenio', login_url='iniciar_sesion', raise_exception=True)
@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
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
            print('asdsad')
            print(_form)
            if form_name == 'form_crear_turno_fijo':
                id_turno = TurnoFijo.objects.latest('id')
                id_turno.calcular_turno_siguiente(id_turno.fecha)
                turnos = []
                invalidas = []
                turnos.append(id_turno)
                fecha = id_turno.fecha + timedelta(days=7)
                while fecha < id_turno.fecha_fin:
                    if turnos[-1].turno_siguiente != None:
                        if turnos[-1].turno_siguiente.fecha == fecha:
                            turnos.append(turnos[-1].turno_siguiente)
                            fecha = turnos[-1].fecha + timedelta(days=7)
                        else:
                            invalidas.append(fecha)
                            fecha = fecha + timedelta(days=7)
                    else:
                        invalidas.append(fecha)
                        fecha = fecha + timedelta(days=7)
                return render(request,'duenio/turno_creado_fijo.html', {'turnos':turnos, 'invalidas':invalidas})
                #return redirect('lista_turno_creado_fijo')
        else:
            contexto[form_name] = klassForm()
    return render(request, ret, contexto)

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def duenio_lista_empleados(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    empleados = Persona.objects.filter(empleado__isnull=False, *mfiltros)
    return render(request, 'empleado/listaEmpleados.html', {'empleados': empleados, "f": ffilter})


@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def modificarComision(request, id):
    persona = get_object_or_404(Persona, pk=id)
    if request.method == "POST":
        persona.empleado.porc_comision = request.POST['NuevaComision']
        persona.empleado.save()
        return redirect('/personas/duenio_lista_empleados')
    else:
        persona = get_object_or_404(Persona, pk=id)
    return render(request, 'empleado/modificarComision.html', {'persona': persona})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def duenio_lista_clientes(request):
    mfiltros, ffilter = get_filtros(Persona, request.GET)
    clientes = Persona.objects.filter(cliente__isnull=False, *mfiltros)
    return render(request, 'duenio/clientes_duenio.html', {'clientes': clientes, "f": ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
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

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def modificar_stock_duenio(request, id):
    insumo = get_object_or_404(Insumo, pk=id)
    if request.method == "POST":
        insumo.stock = request.POST['stockNuevo']
        insumo.save()
        return redirect('/personas/duenio_lista_insumos')
    else:
        insumo = get_object_or_404(Insumo, pk=id)
    return render(request, 'duenio/modificar_stock_duenio.html', {'insumo': insumo})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def duenio_lista_insumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'duenio/insumos_duenio.html', {'insumos': insumos, "f": ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def duenio_lista_turnos(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros).order_by('-fecha')
    return render(request, 'duenio/turnos_duenio.html', {'turnos': turnos, "f": ffilter, 'Turno':Turno})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def duenio_lista_turno_creado_fijo(request, id):
    primero = get_object_or_404(TurnoFijo, pk=id)
    turnos = []
    invalidas =[]
    turnos.append(primero)
    fecha = primero.fecha + timedelta(days=7)
    while fecha < primero.fecha_fin:
        print(fecha)
        print("turno siguiente")
        print(primero.turno_siguiente)
        if turnos[-1].turno_siguiente != None:
            if turnos[-1].turno_siguiente.fecha == fecha:
                turnos.append(turnos[-1].turno_siguiente)
                fecha = turnos[-1].fecha + timedelta(days=7)
                print("agrego a turno")
                print(turnos[-1])
            else:
                invalidas.append(fecha)
                fecha = fecha + timedelta(days=7)
        else:
            invalidas.append(fecha)
            fecha = fecha + timedelta(days=7)
    return render(request, 'duenio/turno_creado_fijo.html', {'turnos': turnos, 'invalidas': invalidas})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def duenio_lista_comisiones(request):
    mfiltros, ffilter = get_filtros(Comision, request.GET)
    comisiones = Comision.objects.filter(*mfiltros)
    return render(request, 'duenio/comisiones_duenio.html', {'comisiones': comisiones, "f": ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def agenda_duenio(request):
    return render(request, 'duenio/agenda_duenio.html', {})


# TODO Ver si esto es realmente necesario.
@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def nuevo_empleado(request):
    return render(request, 'empleado/nuevo_empleado.html', {})


# TODO Ver si esto es realmente necesario.
@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def index_turnos(request):
    return render(request, 'Turnos/index_turnos.html', {})

"""
Vistas del control de cuentas.
"""

def restringido(request):
    return render(request, 'restringido/restringido.html', {})

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
