from django.contrib import admin
from .models import Servico, Categoria

# Register your models here.
admin.site.register(Categoria)
# admin.site.register(Servico)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'preco', 'imagem', 'categoria', 'ativo']

    list_filter = ['categoria', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering = ['nome', 'descricao']
    list_per_page = 25