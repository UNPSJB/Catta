from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from turnos.forms import CrearTurnoForm, ModificarTurnoForm
from turnos.models import Turno
from django.core import serializers

def escupoJSON(request):
    turnos = Turno.objects.all()
    data = serializers.serialize("json", turnos)
    return JsonResponse({
        "turnos": data
    })

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

# TODO pruebas con fullcalendar
def eventosCalendario(request):
    turnos = Turno.objects.all()

    json_lista = []
    for turno in turnos:
        id_t = turno.id
        title = turno.cliente.nombre
        start = turno.fecha

        json_item = {'id': id_t, 'title':title, 'start': start}
        json_lista.append(json_item)

    return HttpResponse(json.dumps(json_lista), content_type='turnos/json')
