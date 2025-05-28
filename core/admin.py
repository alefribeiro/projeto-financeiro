from django.contrib import admin
from core.models.fornecedor import (Estado, Cidade, Fornecedor, TelefonesFornecedor)

class EstadoAdmin(admin.ModelAdmin):
    pass

class CidadeAdmin(admin.ModelAdmin):
    pass

class FornecedorAdmin(admin.ModelAdmin):
    pass

class TelefonesFornecedorAdmin(admin.ModelAdmin):
    list_display = ('fornecedor', 'telefone')
    search_fields = ('fornecedor__nome', 'telefone')

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(TelefonesFornecedor, TelefonesFornecedorAdmin)