from core.models.fornecedor import Fornecedor
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