from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta, time
from django.http import JsonResponse, HttpResponse
from .forms import ModificarTurnoForm
from .models import Turno
from gestion.models import ServicioBasico, Promocion
from django.core import serializers


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


def devuelvo_turnos_libres(request):
    INICIO_TURNO_MAÑANA = time(9, 0)
    FINAL_TURNO_MAÑANA = time(12, 0)
    INICIO_TURNO_TARDE = time(16, 0)
    FINAL_TURNO_TARDE = time(20, 0)
    MODULO = timedelta(minutes=15)

    # Compone la lista con todos los módulos de un día.
    fecha_ingresada = datetime.strptime(request.GET['dia'], "%m/%d/%Y").date()
    inicio_mod = datetime.combine(fecha_ingresada, INICIO_TURNO_MAÑANA)
    fin_mod = datetime.combine(fecha_ingresada, FINAL_TURNO_TARDE)
    horarios = []
    mod = inicio_mod
    while mod < fin_mod:
        if mod.time() == FINAL_TURNO_MAÑANA:
            mod = datetime.combine(mod, INICIO_TURNO_TARDE)
        horarios.append(mod)
        mod += MODULO

    # Obtiene la duración de los servicios y promociones.
    servicios = request.GET.getlist('servicio[]')
    promociones = request.GET.getlist('promocion[]')
    duracion_servicios = timedelta(0)
    for i in servicios:
        servicio = ServicioBasico.objects.all().filter(pk=i)
        duracion_servicios += servicio.first().get_duracion()
    for i in promociones:
        promo = Promocion.objects.all().filter(pk=i)
        duracion_servicios += promo.first().get_duracion()

    # Quita de los horarios disponibles del día los que estan ocupados.
    turnos = Turno.objects.all().filter(fecha__day=fecha_ingresada.day)
    if turnos:
        lista_turnos = []
        for turno in turnos:
            info = {
                'inicio': turno.fecha.time(),
                'fin': turno.get_duracion().time()
            }
            lista_turnos.append(info)
        for hora in reversed(horarios):
            if any(hora.time() >= dato['inicio'] and hora.time() < dato['fin'] for dato in lista_turnos):
                horarios.remove(hora)

    # Compone el JSON y lo devuelve.
    for hora in horarios:
        print(hora)

    return HttpResponse('')

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
    duracion_servicios = timedelta(0)
    for i in servicios:
        servicio = ServicioBasico.objects.all().filter(pk=i)
        duracion_servicios += servicio.first().get_duracion()
    print(duracion_servicios)

    # Compone la respuesta en json.
    for turno in Turno.objects.all().filter(fecha__day=fecha.day):
        inicio_turno = turno.fecha
        fin_turno = turno.get_duracion()
        for m in modulos:
            dato = {}
            if m < fin_turno and m >= inicio_turno:
                if turno.estado() == "Confirmado":  # Si el turno esta confirmado.
                    dato['estado'] = 'confirmado'
                    dato['color'] = '#d9534f'
                else:  # Si el turno no esta confirmado.
                    dato['estado'] = 'no-confirmado'
                    dato['color'] = '#f0ad4e'
            else:  # Si el módulo esta libre.
                dato['estado'] = 'libre'
                dato['color'] = '#5cb85c'
            dato['hora'] = m.hour
            dato['mins'] = m.minute

            datos_json.append(dato)

    return JsonResponse({'modulos': datos_json})
    """

def devuelvo_turnos(request):
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
        form = ModificarTurnoForm(request.POST, instance=turno)
        if form.is_valid:
            form.save()
            redirect('')
    else:
        form = ModificarTurnoForm(instance=turno)

    return render(request, ret, {"form": form})


def listaTurnosFecha(request):
    turnos = Turno.objects.all()
    return render(request, 'confirmarTurno/listaTurnosFecha.html', {'turnos': turnos})


# def confirmar_turno(request, id):
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
    return render(request, 'confirmarTurno/confirmar_turno.html', {'turno': turno})


def calendario(request):
    turnos = Turno.objects.all()
    return render(request, 'calendario/fullcalendar.html', {'turnos': turnos})


"""def detalle_turno(request, id=1):
    turno = get_object_or_404(Turno, pk=id)
    return render(request, 'Turnos/detalle_turno.html', {'turno': turno})
"""
