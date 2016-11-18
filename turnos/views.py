from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.http import JsonResponse
from turnos.forms import ModificarTurnoForm, DetalleTurnoForm
from turnos.models import Turno
from gestion.models import ServicioBasico, Promocion
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


def devuelvo_turnos_libres(request,
                           fecha=datetime.datetime(2016, 1, 1, 0, 0, 0),
                           servicios=[1, 2, 3],
                           promociones=[1, 2, 3]):
    """
    Compone una lista con todos los posibles módulos en un día laboral normal.

    Luego recorre los turnos dados en ese día, quitando de la lista los
    módulos que ya estan ocupados.
    """
    horas_habiles = [9, 10, 11, 12, 16, 17, 18, 19]
    fecha = datetime.datetime(fecha.year, fecha.month, fecha.day, 9, 0, 0)
    modulos = []
    datos_json = []

    delta_minutos = timedelta(minutes=15)

    # Compone la lista genérica con los horarios disponibles.
    for hora in horas_habiles:
        if hora == 12:
            delta_hora = timedelta(hours=4)
            fecha = fecha + delta_hora
        for i in range(4):
            modulos.append(fecha)
            fecha = fecha + delta_minutos

    # Obtiene la duración de los servicios elegidos en conjunto.
    duracion_servicios = 0
    for i in servicios:
        servicio = Servicio.objects.all().filter(id=i)
        duracion_servicios += servicio.get_duracion()

    # Compone la respuesta en json.
    for turno in Turno.objects.all().filter(fecha__day=fecha.day):
        inicio_turno = turno.fecha
        fin_turno = turno.get_duracion()
        for m in modulos:
            dato = {}
            if m < fin_turno and m >= inicio_turno:
                if turno.estado() == "Confirmado":   # Si el turno esta confirmado.
                    dato['estado'] = 'confirmado'
                    dato['color'] = '#d9534f'
                else:   # Si el turno no esta confirmado.
                    dato['estado'] = 'no-confirmado'
                    dato['color'] = '#f0ad4e'
            else:   # Si el módulo esta libre.
                dato['estado'] = 'libre'
                dato['color'] = '#5cb85c'
            dato['hora'] = m.hour
            dato['mins'] = m.minute

            datos_json.append(dato)

    return JsonResponse({'modulos': datos_json})


def devuelvo_turnos(request):
    print(request.GET["start"])
    print(request.GET["end"])
    datos = []
    for turno in Turno.objects.all():
        datos_turno = {
            'id': turno.pk,
            'start': turno.fecha,
            'end': turno.get_duracion(),
            'title': turno.get_cliente(),
            'color': "#f984ce",
            'empleado': turno.get_empleado(),
            'cliente': turno.get_cliente(),
            'servicios': turno.get_servicios(),
            'promociones': turno.get_promociones(),
            'fecha': turno.fecha,
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


#def confirmar_turno(request, id):
#    if request.method == "POST":
#        turno = get_object_or_404(Turno, pk=id)
#        turno.confirmar_turno()
#        turno.save()
#        return redirect('/personas/duenio_lista_turnos')
#    else:
#        turno = get_object_or_404(Turno, pk=id)
#        return render(request, '/turnos/confirmarTurno/confirmar_turno.html', {'turno':turno})


def confirmar_turno(request, id):
    if request.method == "POST":
        turno = get_object_or_404(Turno, pk=id)
        turno.confirmar_turno()
        turno.save()
        return redirect('/personas/duenio_lista_turnos')
    else:
        turno = get_object_or_404(Turno, pk=id)
    return render(request, 'confirmarTurno/confirmar_turno.html', {'turno':turno})



def calendario(request):
    turnos = Turno.objects.all()
    return render(request, 'calendario/fullcalendar.html', {'turnos': turnos})

"""def detalle_turno(request, id=1):
    turno = get_object_or_404(Turno, pk=id)
    return render(request, 'Turnos/detalle_turno.html', {'turno': turno})
"""
