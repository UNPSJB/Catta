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


from .forms import CuentaNuevaForm, EmpleadoNuevoForm, LiquidarComisionForm
from gestion.forms import SectorForm, InsumoForm, ServicioForm, PromoForm
from turnos.forms import CrearTurnoForm, ModificarTurnoForm, RegistrarTurnoRealizadoForm, EliminarTurnoForm, CrearTurnoFijoForm
from .models import Persona, Empleado, Comision, Cliente
from gestion.models import ServicioBasico, Promocion, Insumo, Servicio
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
    return render(request, 'ayuda/ayudaCliente.html')


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
    return render(request, 'ayuda/ayudaEmpleado.html')

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
    return render(request, 'ayuda/ayudaDueño.html')

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def ingreso_neto(request):
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros)
    return render(request, "duenio/ingreso_neto.html", {'turnos': turnos, "f": ffilter})


@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def servicios_mas_solicitados(request):
    pass

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def mes_mayor_trabajo(request):
    pass

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def dia_mayor_trabajo(request):
    dias = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
    mfiltros, ffilter = get_filtros(Turno, request.GET)
    #return render(request, 'duenio/turnos_duenio.html', {'turnos': turnos, "f": ffilter, 'Turno': Turno})
    turnos = Turno.objects.filter(*mfiltros).order_by('-fecha').values("dia").annotate(cant_Dias=Count("dia"))

    for turno in turnos:
        dias[turno['dia'].strftime('%A')] += turno['cant_Dias']

    return render(request,"duenio/dia_mayor_trabajo.html",{'dias':dias,'f':ffilter})

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def dias_mayor_creaciones_turnos(request):
    pass

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def clientes_con_mas_ausencias(request):
    clientes_ausencias = Cliente.objects.annotate(ausencias_turnos = Count(
        Case(
            When (turno__fecha_cancelacion__isnull = False, then =1),
        )
    )).order_by("-ausencias_turnos")
    return render(request, "duenio/clientes_con_mas_ausencias.html", {'clientes' : clientes_ausencias})
    #pass

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def empleados_mas_solicitados(request):
    pass

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_duenio, login_url='restringido', redirect_field_name=None)
def horarios_mas_solicitados(request):


    mfiltros, ffilter = get_filtros(Turno, request.GET)
    turnos = Turno.objects.filter(*mfiltros).order_by('-fecha')
    return render(request, 'duenio/horarios_mas_solicitados.html', {})
    turnos = Turno.objects.values("hora").annotate(horas=Count("hora"))


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


class ListadoPDF(View):
    PAGE_WIDTH  = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

    def cabecera(self, pdf, texto):
        pdf.setFont("Helvetica", 16)
        ancho_texto = stringWidth(texto, "Helvetica", 16)
        pdf.drawString((ListadoPDF.PAGE_WIDTH - ancho_texto) / 2.0, 790, texto)

    def contenido(self, pdf, y):
        pass

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        self.cabecera(pdf)
        y = 760
        self.contenido(pdf, y)

        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response

class ListadoPDFClientes(ListadoPDF):
    def cabecera(self, pdf):
        texto = u"Reporte de Clientes"
        super().cabecera(pdf, texto)

    def get(self, request, query, query1):
        print(query)
        print(query1)

    def contenido(self, pdf, y):
        encabezados = ('DNI', 'Nombre', 'Apellido', 'Localidad', 'Teléfono', 'E-Mail')

        clientes = Persona.objects.filter(cliente__isnull=False)
        detalles = []
        for cliente in clientes:
            y -= 20
            c = (cliente.dni, cliente.nombre, cliente.apellido, cliente.localidad, cliente.telefono, cliente.cliente.email)
            detalles.append(c)

        detalle_orden = Table([encabezados] + detalles)
        detalle_orden.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(3,0),'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 90, y)

class ListadoPDFTurnos(ListadoPDF):
    def cabecera(self, pdf):
        texto = u"Reporte de Turnos"
        super().cabecera(pdf, texto)

    def contenido(self, pdf, y):
        encabezados = ('Fecha y Hora', 'Cliente', 'Empleado', 'Estado', 'Servicios')

        turnos = Turno.objects.all().order_by("-fecha")
        detalles = []

        for turno in turnos:
            y -= 10
            t_servicios = ""

            servicios = turno.servicios.all()
            for i in range(servicios.__len__()):
                y -= 10
                if i == 0 or i == servicios.__len__():
                    t_servicios += servicios[i].nombre
                else:
                    t_servicios += "\n" + servicios[i].nombre

            promos = turno.promociones.all()
            for i in range(promos.__len__()):
                y -= 10
                if i == 0 or i == promos.__len__():
                    t_servicios += promos[i].nombre
                else:
                    t_servicios += "\n" + promos[i].nombre

            c = (turno.fecha, turno.cliente, turno.empleado, turno.estado(), t_servicios)
            detalles.append(c)

        detalle_orden = Table([encabezados] + detalles)
        detalle_orden.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(3,0),'CENTER'),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTSIZE', (0,0), (-1,-1), 10),
            ]
        ))
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 70, y)
