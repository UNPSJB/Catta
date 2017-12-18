from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta, time
from django.http import JsonResponse, HttpResponse
from .forms import ModificarTurnoForm, RegistrarTurnoRealizadoForm
from .models import Turno
from gestion.models import ServicioBasico, Promocion
from django.core import serializers
from datetime import datetime



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
    fecha = datetime.strptime(request.GET['dia'], "%Y-%m-%d").date()
    servicios = request.GET.getlist('servicio[]')
    promociones = request.GET.getlist('promocion[]')
    empleado = request.GET['empleado']
    horarios = Turno.posibles_turnos(fecha, servicios, promociones, empleado)

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
            print("soy cliente")
            turnos = Turno.objects.all().filter(cliente=usuario.persona.cliente)
        else:
            print("soy empleado")
            turnos = Turno.objects.all().filter(empleado=usuario.persona.empleado)
    else:
        print("soy dueña")
        turnos = Turno.objects.all()

    for turno in turnos:

        char = "T"
        fecha = ""
        for letra in str(turno.fecha):
            if letra not in char:
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
    if (request.user.persona.duenia != None):
        user = 'duenia'
    elif (request.user.persona.empleado != None):
        user = 'empleado'
    else:    
        user = 'cliente'
    if request.method == "POST":
        if (request.user.persona.duenia != None):
            ret = '/personas/duenio_lista_turnos'
        else:
            if (request.user.persona.empleado != None):
                ret = '/personas/empleado_lista_turnos'
            else:
                ret = '/personas/cliente_lista_turnos'
        turno = get_object_or_404(Turno, pk=id)
        form = ModificarTurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect(ret)
    else:
        turno = get_object_or_404(Turno, pk=id)
        form = ModificarTurnoForm(instance=turno)
    return render(request, 'modificarTurno/modificar_turno.html', {'turno': turno, "form_modificar_turno": form, 'user':user})


def cancelar_turno(request, id):
        if request.method == "POST":
            if (request.user.persona.duenia != None):
                ret = '/personas/duenio_lista_turnos'
            else:
                if (request.user.persona.empleado != None):
                    ret = '/personas/empleado_lista_turnos'
                else:
                    ret = '/personas/cliente_lista_turnos'
            turno = get_object_or_404(Turno, pk=id)
            turno.cancelar_turno()
            turno.save()
            return redirect(ret)
        else:
            turno = get_object_or_404(Turno, pk=id)
            if (request.user.persona.duenia != None):
                user = 'duenia'
            elif (request.user.persona.empleado != None):
                user = 'empleado'
            else:    
                user = 'cliente'
        return render(request, 'cancelarTurno/cancelar_turno.html', {'turno': turno, 'user':user})



#def listaTurnosFecha(request):
#    turnos = Turno.objects.all()
#    return render(request, 'confirmarTurno/listaTurnosFecha.html', {'turnos': turnos})


def marcar_realizado(request, id):
    if request.method == "POST":
        if (request.user.persona.duenia != None):
            ret = '/personas/duenio_lista_turnos'
        else:
            if (request.user.persona.empleado != None):
                ret = '/personas/empleado_lista_turnos'
            else:
                ret = '/personas/cliente_lista_turnos'
        turno = get_object_or_404(Turno, pk=id)
        turno.realizar_turno()
        form = RegistrarTurnoRealizadoForm(request.POST, instance=turno)
        if form.is_valid:
            form.save()
            return redirect(ret)
    else:
        turno = get_object_or_404(Turno, pk=id)
        form = RegistrarTurnoRealizadoForm(instance=turno)
        if (request.user.persona.duenia != None):
            user = 'duenia'
        elif (request.user.persona.empleado != None):
            user = 'empleado'
        else:    
            user = 'cliente'
    return render(request, 'marcarRealizado/marcar_realizado.html', {'turno': turno, 'form_registrar_turno_realizado': form, 'user':user})


def confirmar_turno(request, id):
    if request.method == "POST":
        if (request.user.persona.duenia != None):
            ret = '/personas/duenio_lista_turnos'
        else:
            if (request.user.persona.empleado != None):
                ret = '/personas/empleado_lista_turnos'
            else:
                ret = '/personas/cliente_lista_turnos'
        turno = get_object_or_404(Turno, pk=id)
        turno.confirmar_turno()
        turno.save()
        return redirect(ret)
    else:
        turno = get_object_or_404(Turno, pk=id)
        if (request.user.persona.duenia != None):
            user = 'duenia'
        elif (request.user.persona.empleado != None):
            user = 'empleado'
        else:    
            user = 'cliente'
    return render(request, 'confirmarTurno/confirmar_turno.html', {'turno': turno, 'user':user})


def calendario(request):
    turnos = Turno.objects.all()
    return render(request, 'calendario/fullcalendar.html', {'turnos': turnos})
