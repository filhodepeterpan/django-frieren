from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.listaContatos, name="contato"),
    path("add-contato", views.addContato, name="addContato"),
    path("del-contato/<int:id_contato>", views.delContato, name="delContato"),
    path("edit-contato/<int:id_contato>", views.editContato, name="editContato"),
]