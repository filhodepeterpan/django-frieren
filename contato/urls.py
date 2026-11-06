from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.addContato, name="contato"),
    path("del-contato/<int:id_contato>", views.delContato, name="delContato"),
    path("edit-contato/<int:id_contato>", views.editContato, name="editContato"),
]
