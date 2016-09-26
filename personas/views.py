from django.shortcuts import render

def index(request):
    return render(request, 'principal/index.html', {})

def login(request):
    return render(request, 'login/login.html', {})

def cuenta(request):
    return render(request, 'cuentaNueva/cuenta_nueva.html', {})

def empleado(request):
    return render(request, 'empleado/index_empleado.html', {})
