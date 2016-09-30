from django.shortcuts import render

def index(request):
    return render(request, 'principal/index.html', {})

def login(request):
    return render(request, 'login/login.html', {})

def cuenta(request):
    return render(request, 'cuentaNueva/cuenta_nueva.html', {})

def empleado(request):
    return render(request, 'empleado/index_empleado.html', {})

def nuevo_empleado(request):
    return render(request, 'empleado/nuevo_empleado.html', {})

def duenio(request):
    return render(request, 'duenio/index_duenio.html', {})

def cliente(request):
    return render(request, 'cliente/index_cliente.html', {})

def nuevo_cliente(request):
    return render(request, 'cliente/nuevo_cliente.html', {})

def sector(request):
    return render(request, 'sector/sector.html', {})

def index_turnos(request):
	return render(request, 'Turnos/index_turnos.html', {})
