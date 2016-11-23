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
    fecha_ingresada = datetime.strptime(request.GET['dia'], "%d/%m/%Y").date()
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
    empleado = request.GET['empleado']
    turnos = Turno.objects.all().filter(fecha__day=fecha_ingresada.day, empleado=empleado)
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
    datos_json = []
    for hora in horarios:
        dato = {
            'estado': 'libre',
            'hora': hora.hour,
            'mins': hora.minute,
            'color': '#5cb85c'
        }
        datos_json.append(dato)

    return JsonResponse({'modulos': datos_json})


def devuelvo_turnos(request):
    datos = []
    usuario = request.user

    if usuario.persona.duenia == None:
        if usuario.persona.empleado == None:
            turnos = Turno.objects.all().filter(empleado=usuario.persona.empleado)
        else:
            turnos = Turno.objects.all().filter(cliente=usuario.persona.empleado)
    else:
        turnos = Turno.objects.all()

    for turno in turnos:

        vocales = "T"
        fecha = ""
        for letra in str(turno.fecha):
            if letra not in vocales:
                fecha += letra

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
            'fecha': fecha,
        }
        datos.append(datos_turno)
    return JsonResponse({'turnos': datos})


def modificar_turno(request, id):
    if request.method == "POST":
        turno = get_object_or_404(Turno, pk=id)
        form = ModificarTurnoForm(request.POST, instance=turno)
        if form.is_valid:
            form.save()
            return redirect('/personas/duenio_lista_turnos')
    else:
        turno = get_object_or_404(Turno, pk=id)
        form = ModificarTurnoForm(instance=turno)
    return render(request, 'modificarTurno/modificar_turno.html', {'turno': turno, "form_modificar_turno": form})

def cancelar_turno(request, id):
        if request.method == "POST":
            turno = get_object_or_404(Turno, pk=id)
            turno.cancelar_turno()
            turno.save()
            return redirect('/personas/duenio_lista_turnos')
        else:
            turno = get_object_or_404(Turno, pk=id)
        return render(request, 'cancelarTurno/cancelar_turno.html', {'turno': turno})


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
