from django.shortcuts import render

def sector(request):
    return render(request, 'sector/sector.html', {})
