from django.shortcuts import render, redirect
from turnos.forms import TurnoForm
from turnos.models import Turno


def turno(request):
    if request.method == "POST":
        form_turno = TurnoForm(request.POST)
        if form_turno.is_valid():
            form_turno.save()
            return redirect('/duenio')
        print(form_turno)
    else:
        form_turno = TurnoForm()
    return render(request, 'sector/altaSector.html', {"form": form_turno})

def escupoJSON(request):
    return render(request, 'escupoJSON/escupoJSON.html', {})
