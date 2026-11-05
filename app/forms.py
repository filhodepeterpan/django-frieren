from django import forms
from .models import Servico

class FormServico(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ("nome","descricao","preco", "categoria", "imagem", "ativo")