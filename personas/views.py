from django import forms
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Q, Count
from django.views.generic import View
from django.http import HttpResponse
from datetime import datetime, date, time, timedelta
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import stringWidth
from django.db.models import Case, When
from easy_pdf.views import PDFTemplateView
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json


from .forms import CuentaNuevaForm, EmpleadoNuevoForm, LiquidarComisionForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm, PromoForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm, RegistrarTurnoRealizadoForm, EliminarTurnoForm, CrearTurnoFijoForm
from .models import Persona, Empleado, Comision, Cliente
from gestion.models import ServicioBasico, Promocion, Insumo, Servicio, Sector
from turnos.models import Turno, TurnoFijo




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

def ayuda_externa(request):
    return render(request, 'ayuda/ayudaExterna.html')

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


@login_required(login_url='iniciar_sesion')
@user_passes_test(es_cliente, login_url='restringido', redirect_field_name=None)
def ayuda_cliente(request):
    contexto = {}
    contexto['cliente'] = True
    contexto['logeado'] = True
    return render(request, 'ayuda/ayudaCliente.html', contexto)


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
                    return render(request,'empleado/turno_creado_fijo_empleado.html', {'turnos':turnos, 'invalidas':invalidas})
                redirect(usuario.get_vista())
            contexto[form_name] = _form
            contexto["formularioError"] = input_name

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

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_empleado, login_url='restringido', redirect_field_name=None)
def ayuda_empleado(request):
    contexto = {}
    contexto['empleado'] = True
    contexto['logeado'] = True
    return render(request, 'ayuda/ayudaEmpleado.html',contexto)

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
            contexto[form_name] = _form
            contexto["formularioError"] = input_name

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
    servicios1 = []
    for servicio in servicios:
        nombre = servicio.nombre
        esta = False
        for serviox in servicios1:
            if serviox.nombre == nombre:
                esta = True
        if not esta:
            servicios1.append(servicio)
            for servicio2 in servicios:
                nombre1 = servicio2.nombre
                if nombre == nombre1:
                    if servicio.id < servicio2.id:
                        long = len(servicios1)
                        servicios1[long - 1] = servicio2
    promociones = Promocion.objects.filter(*mfiltros)
    insumos = Insumo.objects.all()

    topServicios = ServicioBasico.objects.annotate(cantidad_de_turnos=Count("turnos")).order_by("-cantidad_de_turnos")[:5]

    return render(request, 'duenio/servicios_duenio.html', {'servicios': servicios1,
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
    query = 'Turno.objects.filter(*mfiltros).order_by(\'-fecha\'))'
    query1 = str(mfiltros)
    return render(request, 'duenio/turnos_duenio.html', {'query':query,'query1':query1,'turnos': turnos, "f": ffilter, 'Turno':Turno})

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

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def ayuda_duenio(request):
    contexto = {}
    contexto['dueño'] = True
    contexto['logeado'] = True
    return render(request, 'ayuda/ayudaDueño.html',contexto)

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def ingreso_neto(request):
    contexto = {}
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros)
    #FALTA SABER COMO FILTRAR LOS TURNOS SEGUN EL ESTADO
    servicios = ServicioBasico.objects.all()
    contexto['turnos'] = turnos
    contexto['servicios'] = servicios
    contexto['f'] = ffilter
    return render(request, "duenio/ingreso_neto.html", contexto)


@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def servicios_mas_solicitados(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    try:
        fecha_inicio = ffilter['fechaI']
    except KeyError:
        fecha_inicio = "2010-01-01"

    try:
        fecha_fin = ffilter['fechaF']
    except KeyError:
        hoy = datetime.today()
        fecha_fin = str(hoy.year) + "-" + str(hoy.month) + "-" + str(hoy.day)

    servicios = ServicioBasico.objects.annotate(cantidad_de_turnos=Count(
            Case(
                When(turnos__fecha__gt=fecha_inicio,
                     turnos__fecha__lt=fecha_fin,
                     then=1)
            )
    )).order_by("-cantidad_de_turnos")[:5]

    return render(request, "duenio/servicios_mas_solicitados.html", {'servicios': servicios, "f": ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def mes_mayor_trabajo(request):
    contexto = {}
    meses = {'January': 0, 'Februry': 0, 'March': 0, 'April': 0,
             'May': 0, 'June': 0, 'July': 0, 'August':0,
             'September':0, 'Octuber':0, 'November':0, 'December':0}
    #FALTA FIJARSE QUE EL TURNO REALMENTE SE HAYA REALIZADO
    turnos = Turno.objects.all()
    for turno in turnos:
        try:
            meses[turno.fecha_realizacion.strftime('%B')] += 1
        except AttributeError:
            pass                        
        except KeyError:
            meses[turno.fecha_realizacion.strftime('%B')] = 1                        
    contexto['meses'] = meses
    return render(request, 'duenio/mes_mayor_trabajo.html', contexto)

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def dia_mayor_trabajo(request):
    dias = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
    #FALTA FIJARSE QUE EL TURNO REALMENTE SE HAYA REALIZADO
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros).order_by('-fecha').values("dia").annotate(cant_Dias=Count("dia"))

    for turno in turnos:
        dias[turno['dia'].strftime('%A')] += turno['cant_Dias']

    return render(request,"duenio/dia_mayor_trabajo.html",{'dias':dias,'f':ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def dias_mayor_creaciones_turnos(request):
    contexto = {}
    dias = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros)
    for turno in turnos:
        try:
            dias[turno.fecha_creacion.strftime('%A')] += 1
        except KeyError:
            dias[turno.fecha_creacion.strftime('%A')] = 1                        
    contexto['dias'] = dias
    return render(request, 'duenio/dias_mayor_creaciones_turnos.html', contexto)

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def clientes_con_mas_ausencias(request):
    contexto = {}
    clientes_ausencias = Cliente.objects.annotate(ausencias_turnos = Count(
        Case(
            When (turno__fecha_cancelacion__isnull = False, then = 1),
        )
    )).order_by("-ausencias_turnos")[:5]
    contexto['clientes'] = clientes_ausencias
    return render(request, "duenio/clientes_con_mas_ausencias.html", contexto)
    #pass

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def empleados_mas_solicitados(request):
    contexto = {}
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    try:
        sector = ffilter['sector']
    except KeyError:
        sector = "*"
    try:
        fecha_inicio = ffilter['fechaI']
    except KeyError:
        fecha_inicio = "2000-01-01"
    try:
        fecha_fin = ffilter['fechaF']
    except KeyError:
        fecha_fin = "9999-01-01"
    if sector=="*":
        topEmplados = Empleado.objects.annotate(cantidad_de_turnos=Count(
            Case(
                When(turno__fecha_realizacion__isnull=False,
                        turno__fecha__gt=fecha_inicio,
                        turno__fecha__lt=fecha_fin,
                        then=1),
            )
        )).order_by("-cantidad_de_turnos")[:5]
    else:
        topEmplados = Empleado.objects.annotate(cantidad_de_turnos=Count(
            Case(
                When(turno__fecha_realizacion__isnull=False,
                        turno__fecha__gt=fecha_inicio,
                        turno__fecha__lt=fecha_fin,
                        sector=sector,
                        then=1),
            )
        )).order_by("-cantidad_de_turnos")[:5]
    todos_los_sectores = Sector.objects.all()
    contexto['sectores'] = todos_los_sectores
    contexto['empleados'] = topEmplados
    data = serializers.serialize("json", topEmplados)
    request.session['empleados'] = data
    datos = json.dumps(list(topEmplados.values()), cls=DjangoJSONEncoder)
    request.session['datos'] = datos
    return render(request, "duenio/empleados_mas_solicitados.html", contexto)

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def horarios_mas_solicitados(request):
    contexto = {}
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    horarios_mas_solicitados = Turno.objects.filter(*mfiltros).values("hora").annotate(cantidad_de_turnos=Count("hora"))
    contexto['horarios'] = horarios_mas_solicitados
    return render(request, 'duenio/horarios_mas_solicitados.html', contexto)

"""
Vistas de Reportes para convertir a PDF
"""

class EmpleadosMasSolicitadosPDF(PDFTemplateView):
    template_name = 'reportesPDF/empleados_mas_solicitados_pdf.html'

    def get_context_data(self, **kwargs):
        context = super(EmpleadosMasSolicitadosPDF, self).get_context_data(**kwargs)
        empleados=[]
        for obj in serializers.deserialize("json", self.request.session['empleados']):
            empleados.append(obj.object)

        cantidad_de_turnos=[]
        datos = json.loads(self.request.session['datos'])
        for dato in datos:
            cantidad_de_turnos.append(dato['cantidad_de_turnos'])

        datos=[]

        for empleado,cantidad in zip(empleados, cantidad_de_turnos):
            datos.append((empleado, cantidad))
        context['datos'] = datos
        return context


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
