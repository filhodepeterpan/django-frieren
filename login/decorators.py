from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Perfil

def admin_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        perfil = Perfil.objects.get(usuario=request.user)

        if perfil.tipo_usuario != 'administrador':
            return redirect("dashboard")

        return view(request, *args, **kwargs)

    return wrapper
