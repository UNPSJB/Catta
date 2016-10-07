from django.shortcuts import render, redirect
from gestion.forms import SectorForm
from gestion.forms import InsumoForm
from gestion.forms import ServicioForm

def sector(request):
    if request.method == "POST":
        form = SectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/duenio')
        print(form)
    else:
        form = SectorForm()
    return render(request, 'sector/sector.html', {"form": form})

def insumo(request):
    if request.method == "POST":
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/duenio')
        print(form)
    else:
        form = InsumoForm()
    return render(request, 'insumo/insumo.html', {"form": form})

def servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/duenio')
        print(form)
    else:
        form = ServicioForm()
    return render(request, 'servicio/servicio.html', {"form": form})
