from django.contrib import admin
from core.models.fornecedor import (Estado, Cidade, Fornecedor, TelefonesFornecedor)
from core.models.lancamento import (
    FormaPagamento,
    Categoria,
    Lancamento
)

class EstadoAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Estado

class CidadeAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Cidade

class FornecedorAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Fornecedor
        

class FormaPagamentoAdmin(admin.ModelAdmin):
    
    class Meta:
        model = FormaPagamento
        
        
class CategoriaAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Categoria

class LancamentoAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Lancamento

class TelefonesFornecedorAdmin(admin.ModelAdmin):
    list_display = ('fornecedor', 'telefone')
    search_fields = ('fornecedor__nome', 'telefone')

    class Meta:
        model = TelefonesFornecedor

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(FormaPagamento, FormaPagamentoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(TelefonesFornecedor, TelefonesFornecedorAdmin)
admin.site.register(Lancamento, LancamentoAdmin)