from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CadastroForm
from .models import Perfil
from django.contrib import messages

def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(usuario=usuario, tipo_usuario='cliente')
            return redirect("login")
    else:
        form = CadastroForm()

    return render(request, "cadastro.html", {"form":form})

@login_required
def dashboard(request):
    perfil = Perfil.objects.get(usuario=request.user)

    if perfil.tipo_usuario == 'administrador':
        return redirect("/admin")

    return render(request, "dashboard.html")

@login_required
def perfil(request):

    if request.method == "POST":
        usuario = request.user

        usuario.first_name = request.POST.get("nome")
        usuario.last_name = request.POST.get("sobrenome")
        usuario.email = request.POST.get("email")

        usuario.save()
        return redirect("dashboard")

    return render(request, "perfil.html")


