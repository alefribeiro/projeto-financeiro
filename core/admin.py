from django.contrib import admin
from core.models.fornecedor import (Estado, Cidade, FornecedorModel)

class EstadoAdmin(admin.ModelAdmin):
    pass

class CidadeAdmin(admin.ModelAdmin):
    pass

class FornecedorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(FornecedorModel, FornecedorAdmin)