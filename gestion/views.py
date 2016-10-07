from django.shortcuts import render, redirect
from gestion.forms import SectorForm

def sector(request):
    if request.method == "POST":
        form = SectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/duenio')
        print(form)
    else:
        form = SectorForm()
    return render(request, 'sector/sector.html', {"form": form})
