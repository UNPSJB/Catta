from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServicioForm, ModificarServicioForm, InsumoForm, SectorForm
from .models import ServicioBasico, Servicio, Promocion
from .models import Insumo
from django.db.models import Q
from django.contrib import messages


def sector(request):
    if request.method == "POST":
        form = SectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/duenio')
        print(form)
    else:
        form = SectorForm()
    return render(request, 'sector/altaSector.html', {"form": form})


def insumo(request):
    if request.method == "POST":
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/duenio')
        print(form)
    else:
        form = InsumoForm()
    return render(request, 'insumo/altaInsumo.html', {"form": form})


def servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST, request.FILES or None)
        if form.is_valid():
            servicio = form.save()
            servicio.save()
            # messages.success(request, "Servicio creado")  # from django.contrib import messages
            return redirect(servicio.get_vista())
    else:
        form = ServicioForm()
    return render(request, 'servicio/altaServicio.html', {"form": form})


def listaServicios(request):
    if (request.user.persona.duenia != None):
        usuario = 'duenia'
    elif (request.user.persona.empleado != None):
        usuario = 'empleado'
    else:
        usuario = 'cliente'
    servicios = ServicioBasico.objects.all()
    insumos = Insumo.objects.all()
    return render(request, 'servicio/listaServicios.html', {'servicios': servicios, 'insumos': insumos, 'usuario': usuario})


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

def modificar_servicio(request, id):
    if request.method == "POST":
        if (request.user.persona.duenia != None):
            ret = '/personas/duenio_lista_servicios'
        else:
            if (request.user.persona.empleado != None):
                ret = '/personas/empleado_lista_servicios'
            else:
                ret = '/personas/cliente_lista_servicios'
        servicio = get_object_or_404(ServicioBasico, pk=id)
        servicio_nuevo = ServicioBasico()
        servicio_nuevo.nombre = servicio.nombre
        servicio_nuevo.sector = servicio.sector
        form = ModificarServicioForm(request.POST, instance=servicio_nuevo)
        if form.is_valid():
            form.save()
            return redirect(ret)
    else:
        servicio = get_object_or_404(ServicioBasico, pk=id)
        form = ModificarServicioForm(instance=servicio)
    return render(request, 'servicio/modificar_servicio.html', {'servicio': servicio, "form_modificar_servicio": form})

def activar_promocion(request, id):
    if request.method == "POST":
        if (request.user.persona.duenia != None):
            ret = '/personas/duenio_lista_servicios'
        else:
            if (request.user.persona.empleado != None):
                ret = '/personas/empleado_lista_servicios'
            else:
                ret = '/personas/cliente_lista_servicios'
        promocion = get_object_or_404(Promocion, pk=id)
        promocion.activa = True
        promocion.save()
        return redirect(ret)
    else:
        promocion = get_object_or_404(Promocion, pk=id)
        if (request.user.persona.duenia != None):
            user = 'duenia'
        elif (request.user.persona.empleado != None):
            user = 'empleado'
        else:
            user = 'cliente'
    return render(request, 'servicio/activar_promocion.html', {'promocion': promocion, 'user': user})


def desactivar_promocion(request, id):
    if request.method == "POST":
        if (request.user.persona.duenia != None):
            ret = '/personas/duenio_lista_servicios'
        else:
            if (request.user.persona.empleado != None):
                ret = '/personas/empleado_lista_servicios'
            else:
                ret = '/personas/cliente_lista_servicios'
        promocion = get_object_or_404(Promocion, pk=id)
        promocion.activa = False
        promocion.save()
        return redirect(ret)
    else:
        promocion = get_object_or_404(Promocion, pk=id)
        if (request.user.persona.duenia != None):
            user = 'duenia'
        elif (request.user.persona.empleado != None):
            user = 'empleado'
        else:
            user = 'cliente'
    return render(request, 'servicio/desactivar_promocion.html', {'promocion': promocion, 'user': user})


def listaInsumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'insumo/listaInsumos.html', {'insumos': insumos, "f": ffilter})


def modificarStockInsumo(request, id):
    insumo = get_object_or_404(Insumo, pk=id)
    if request.method == "POST":
        insumo.stock = request.POST['stockNuevo']
        insumo.save()
        return redirect('/personas/empleado_lista_insumos')
    else:
        insumo = get_object_or_404(Insumo, pk=id)
        if (request.user.persona.duenia != None):
            user = 'duenia'
        else:
            user = 'empleado'
    return render(request, 'insumo/modificarStockInsumo.html', {'insumo': insumo, 'user':user})


def eliminarInsumo(request, id):
    insumo = get_object_or_404(Insumo, pk=id)
    insumos = insumo.serviciobasico_set.all()
    if request.method == "POST":
        if insumos.first == None :
            insumo.delete()
            return redirect('/personas/duenio_lista_insumos')
        else:
            print('asd')
            messages.warning(request, 'no se puede eliminar el insumo')
    return render(request, 'insumo/eliminarInsumo.html', {'insumo': insumo})


def detalleServicio(request, id):
    servicio = get_object_or_404(ServicioBasico, nombre=id)
    return render(request, 'insumo/modificarStockInsumo.html', {'servicio': servicio})
