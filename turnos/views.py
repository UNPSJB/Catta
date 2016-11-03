from django.shortcuts import render, redirect
from django.http import JsonResponse
from turnos.forms import CrearTurnoForm, ModificarTurnoForm, ConfirmarTurnoForm
from turnos.models import Turno
from django.core import serializers

import json
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
    turnos = Turno.objects.all()

    datos = []
    for turno in turnos:
        datos_turno = {
            'id': turno.pk,
            'start': turno.fecha,
            'end': turno.get_duracion()
        }
        datos.append(datos_turno)
    return JsonResponse({'turnos': json.dumps(datos, default=manejador_fechas)})

def modificar_turno(request, id_turno=1):
    turno = Turno.objects.get(id=id_turno)
    #usuario = request.user()
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

def confirmar_turno(request, id_turno=1):
    turno = Turno.objects.get(id=id_turno)
    #usuario = request.user()
    ret = "turnos/confirmarTurno.html"
    if request.method == "POST":
        form = ConfirmarTurnoForm(request.POST, instance=turno)
        if form.is_valid:
            form.save()
            return redirect('/turnos/confirmarTurno')
    else:
        form = ConfirmarTurnoForm(instance=turno)
    return render(request, ret, {"turno": turno})