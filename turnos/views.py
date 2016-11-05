from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from turnos.forms import ModificarTurnoForm
from turnos.models import Turno
from django.core import serializers

import datetime


def escupoJSON(request):
    turnos = Turno.objects.all()
    data = serializers.serialize("json", turnos)
    return JsonResponse({
        "turnos": data
    })


def manejador_fechas(fecha):
    if isinstance(fecha, datetime.datetime):
        return fecha.isoformat()
    raise TypeError("Tipo desconocido")


def devuelvo_turnos(request):
    print(request.GET["start"])
    print(request.GET["end"])
    datos = []
    for turno in Turno.objects.all():
        datos_turno = {
            'id': turno.pk,
            'start': turno.fecha,
            'end': turno.get_duracion(),
            'title': str(turno)
        }
        datos.append(datos_turno)
    return JsonResponse({'turnos': datos})


def modificar_turno(request, id_turno=1):
    turno = Turno.objects.get(id=id_turno)
    # usuario = request.user()
    ret = "empleado/index_empleado.html"
    if request.method == "POST":
        print('cagamos')
        form = ModificarTurnoForm(request.POST, instance=turno)
        if form.is_valid:
            form.save()
            redirect('')
    else:
        form = ModificarTurnoForm(instance=turno)
        print('entre')

    return render(request, ret, {"form": form})


def listaTurnosFecha(request):
    turnos = Turno.objects.all()
    return render(request, 'confirmarTurno/listaTurnosFecha.html', {'turnos':turnos})


def confirmar_turno(request, id):
    turno = get_object_or_404(Turno, pk=id)
    if request.method == "POST":
        turno.confirmar_turno()
        turno.save()
        return redirect('/Turnos/confirmar_turno.html')
    else:
        turno = get_object_or_404(Turno, pk=id)
    return render(request, 'Turnos/confirmar_turno.html', {'turno':turno})


def calendario(request):
    turnos = Turno.objects.all()
    return render(request, 'calendario/fullcalendar.html', {'turnos': turnos})
