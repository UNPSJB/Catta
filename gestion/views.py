from django.shortcuts import render, redirect, get_object_or_404
from gestion.forms import SectorForm
from gestion.forms import InsumoForm
from gestion.forms import ServicioForm
from gestion.models import ServicioBasico
from gestion.models import Insumo


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


def listaInsumos(request):
    insumos = Insumo.objects.all()

    # if request.method == "POST":
    #     return redirect('/insumo/modificarStockInsumo')

    return render(request, 'insumo/listaInsumos.html', {'insumos': insumos})


def modificarStockInsumo(request, id):
    insumo = get_object_or_404(Insumo, pk=id)
    if request.method == "POST":
        insumo.stock = request.POST['stockNuevo']
        insumo.save()
        return redirect('/gestion/listaInsumos')
    else:
        insumo = get_object_or_404(Insumo, pk=id)
    return render(request, 'insumo/modificarStockInsumo.html', {'insumo': insumo})


def detalleServicio(request, id):
    servicio = get_object_or_404(ServicioBasico, nombre=id)
    return render(request, 'insumo/modificarStockInsumo.html', {'servicio': servicio})
