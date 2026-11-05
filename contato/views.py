from django.shortcuts import redirect, render

from contato.forms import FormContato
from .models import Contato

def listaContatos(request):
    contatos = Contato.objects.all()
    return render(request, "contato.html", {'contatos':contatos})

def addContato(request):
    form = FormContato(request.POST or None, request.FILES or None)

    if request.POST:
        if form.is_valid():
            form.save()

        return redirect("contato")

    return render(request, "add-contato.html", {'form':form})

def delContato(request, id_contato):
    contato = Contato.objects.get(id=id_contato)

    if contato:
        contato.delete()

    return redirect("contato")

def editContato(request, id_contato):
    contato = Contato.objects.get(id=id_contato)
    form = FormContato(request.POST or None, request.FILES or None, instance=contato)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("contato")

    return render(request, "edit-contato.html", {'form':form})
