from django.contrib import admin
from core.models import (Estado, Cidade, Fornecedor)

class EstadoAdmin(admin.ModelAdmin):
    pass

class CidadeAdmin(admin.ModelAdmin):
    pass

class FornecedorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)