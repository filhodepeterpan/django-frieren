from django.shortcuts import redirect, render
from django.contrib import messages
from login.decorators import admin_required

from contato.forms import FormContato
from .models import Contato

def addContato(request):
    form = FormContato(request.POST or None)

    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("contato")

    return render(request, "contato.html", {'form':form})

@admin_required
def delContato(request, id_contato):
    contato = Contato.objects.get(id=id_contato)

    if contato:
        contato.delete()

    return redirect("contatos")

@admin_required
def editContato(request, id_contato):
    contato = Contato.objects.get(id=id_contato)
    form = FormContato(request.POST or None, instance=contato)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("contatos")

    return render(request, "edit-contato.html", {'form':form})
