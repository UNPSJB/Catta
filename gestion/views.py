from django.shortcuts import render, redirect, get_object_or_404
from gestion.forms import SectorForm
from gestion.forms import InsumoForm
from gestion.forms import ServicioForm
from gestion.models import ServicioBasico
from gestion.models import Insumo
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
            return redirect('/duenio')
    else:
        form = ServicioForm()
    return render(request, 'servicio/altaServicio.html', {"form": form})


def listaServicios(request):
    servicios = ServicioBasico.objects.all()
    insumos = Insumo.objects.all()
    return render(request, 'servicio/listaServicios.html', {'servicios': servicios, 'insumos': insumos})


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


def listaInsumos(request):
    mfiltros, ffilter = get_filtros(Insumo, request.GET)
    insumos = Insumo.objects.filter(*mfiltros)
    return render(request, 'insumo/listaInsumos.html', {'insumos': insumos, "f": ffilter})


def modificarStockInsumo(request, id):
    insumo = get_object_or_404(Insumo, pk=id)
    if request.method == "POST":
        insumo.stock = request.POST['stockNuevo']
        insumo.save()
        return redirect('/personas/duenio_lista_insumos')
    else:
        insumo = get_object_or_404(Insumo, pk=id)
    return render(request, 'insumo/modificarStockInsumo.html', {'insumo': insumo})

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
