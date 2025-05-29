from core.models.fornecedor import Fornecedor, TelefonesFornecedor
from core.repository.base import BaseRepository

class FornecedorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Fornecedor)

    
    def get_all(self):
        return self.model.objects.all()
    
    def get_by_id(self, pk):
        return self.model.objects.get(pk=pk)
    
    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)
    
    def update(self, pk, **kwargs):
        fornecedor = self.get_by_id(pk)
        for key, value in kwargs.items():
            setattr(fornecedor, key, value)
        fornecedor.save()
        return fornecedor
    
    def listar_telefones_por_fornecedor(fornecedor):
        return fornecedor.telefones.all()

    
    def criar_telefone(fornecedor, numero):
        return TelefonesFornecedor.objects.create(fornecedor=fornecedor, telefone=numero)

    
    def atualizar_telefones(telefones):
        return TelefonesFornecedor.objects.bulk_update(telefones, ['telefone'])

    
    def deletar_telefones_por_ids(fornecedor, ids):
        return fornecedor.telefones.filter(id__in=ids).delete()