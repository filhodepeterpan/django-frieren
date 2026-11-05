from django.shortcuts import render, redirect
from .models import Servico, Categoria
from .forms import FormServico
from .supabase_client import supabase
from .serializers import CategoriaSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Sum, Count
import requests

# Create your views here.

def index(request):
    return render(request, "index.html")

def servicos(request):
    # servicos = Servico.objects.all()
    servicos = Servico.objects.filter(ativo=True)
    servicos = servicos.exclude(preco=0)

    total_servicos = servicos.count()
    tem_servicos = servicos.exists()

    mais_barato = servicos.order_by('preco').first()
    mais_caro = servicos.order_by('-preco').first()

    busca = request.GET.get('busca')

    if busca:
        servicos = servicos.filter(nome__icontains=busca)
    
    categorias = Categoria.objects.filter(ativo=True)
    categoria = request.GET.get('categoria')

    if categoria:
        servicos = servicos.filter(categoria_id=categoria)
    
    preco = request.GET.get('preco')

    if preco == 'baixo':
        servicos = servicos.filter(preco__lte=500)
    elif preco == 'medio':
        servicos = servicos.filter(
            preco__gte=500,
            preco__lte=1500
        )
    elif preco == 'alto':
        servicos = servicos.filter(preco__gt=1500)

    ordem = request.GET.get('ordem')

    if ordem == 'menor':
        servicos = servicos.order_by('preco')
    elif ordem == 'maior':
        servicos = servicos.order_by('-preco')
    elif ordem == 'nome':
        servicos = servicos.order_by('nome')
    else:
        servicos = servicos.order_by('nome')

    context = {
        'servicos' : servicos,
        'total_servicos' : total_servicos,
        'tem_servicos' : tem_servicos,
        'mais_barato' : mais_barato,
        'mais_caro' : mais_caro,
        'categoria' : categoria,
        'categorias' : categorias,
        'preco' : preco,
        'ordem' : ordem
    }

    return render(request, "servicos.html", context)

def produtos(request):
    servicos = Servico.objects.all()

    # requisição
    resposta = requests.get('https://fakestoreapi.com/products')
    produtos_api = resposta.json()

    return render(request, "produtos.html", {'produtos':servicos, 'produtos_api': produtos_api})

def addServico(request):
    form = FormServico(request.POST or None, request.FILES or None)

    if request.POST:
        if form.is_valid():
            form.save()

        return redirect("servicos")

    return render(request, "add-servico.html", {'form':form})

def delServico(request, id_servico):
    servico = Servico.objects.get(id=id_servico)

    if servico:
        servico.delete()

    return redirect("servicos")

def editServico(request, id_servico):
    servico = Servico.objects.get(id=id_servico)
    form = FormServico(request.POST or None, request.FILES or None, instance=servico)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("servicos")

    return render(request, "edit-servico.html", {'form':form})

def integrantes(request):
    resposta = (supabase
        .table("integrantes")
        .select("*")
        .execute())

    return render(request, "integrantes.html", {'integrantes':resposta.data})

def addIntegrante(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")
        biografia = request.POST.get("biografia")
        foto = request.POST.get("foto")

        supabase.table("integrantes").insert({
            "nome" : nome,
            "cargo" : cargo,
            "biografia" : biografia,
            "foto_url" : foto
        }).execute()

        return redirect("integrantes")

    return render(request, "add-integrante.html")

def delIntegrante(request, id_integrante):
    supabase.table("integrantes").delete().eq("id" , id_integrante).execute()
    return redirect("integrantes")

@api_view(['GET', 'POST'])
def categoriasAPI(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
def categoriaAPI(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer.CategoriaSerializer(categoria, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def relatorios(request):
    servicos = Servico.objects.all()
    servicos_ativos = servicos.filter(ativo=True).count()
    servicos_inativos = servicos.filter(ativo=False).count()

    categorias = (servicos.values('categoria__nome').annotate(quantidade=Count('id')))

    return render(request, 'relatorio.html', {
        'servicos_ativos' : servicos_ativos,
        'servicos_inativos' : servicos_inativos,
        'categorias_labels' : [
            item['categoria__nome'] or 'Sem categoria'
            for item in categorias
        ],
        'categorias_valores' : [
            item['quantidade']
            for item in categorias
        ]
    })