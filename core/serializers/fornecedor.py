from rest_framework import serializers
from core.models.fornecedor import Fornecedor, Estado, Cidade, TelefonesFornecedor
import requests
from core.repository.fornecedor import FornecedorRepository

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['nome', 'uf']


class CidadeSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = Cidade
        fields = ['nome', 'estado']

class TelefonesFornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelefonesFornecedor
        fields = ['id', 'telefone'] 
class FornecedorSerializer(serializers.ModelSerializer):
    fornecedor_repository = FornecedorRepository()
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['cidade'] = CidadeSerializer(instance.cidade).data
        rep['telefones'] = TelefonesFornecedorSerializer(instance.telefones.all(), many=True).data
        return rep
    
    class Meta:
        model = Fornecedor
        fields = '__all__'    

    def create(self, validated_data):
        response_cnpj = requests.get(f'https://receitaws.com.br/v1/cnpj/{validated_data.get('cnpj')}')  

        if response_cnpj.status_code == 200:

            dados_convertidos = response_cnpj.json()
            
            validated_data['logradouro'] = dados_convertidos.get('logradouro', '')
            validated_data['telefone'] = dados_convertidos.get('telefone', '')  
            validated_data['complemento'] = dados_convertidos.get('complemento', '')
            validated_data['bairro'] = dados_convertidos.get('bairro', '')
            validated_data['cep'] = dados_convertidos.get('cep', '')
        
        return self.fornecedor_repository.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        dados_telefones_recebidos = self.initial_data.get('telefones', [])
       
        fornecedor = super().update(instance, validated_data)
        
        mapa_telefones_existentes = {tel.id: tel for tel in fornecedor.telefones.all()}
        
        telefones_para_atualizar = []
        ids_telefones_recebidos = set() 

        for dados_item_telefone in dados_telefones_recebidos:
            id_telefone = dados_item_telefone.get('id')
            
            if id_telefone and id_telefone in mapa_telefones_existentes:
                
                ids_telefones_recebidos.add(id_telefone)
                objeto_telefone = mapa_telefones_existentes[id_telefone]
                
                objeto_telefone.telefone = dados_item_telefone.get('telefone', objeto_telefone.telefone)
                telefones_para_atualizar.append(objeto_telefone)
            else:
                FornecedorRepository.criar_telefone(fornecedor, dados_item_telefone['telefone'])

        
        if telefones_para_atualizar:
            FornecedorRepository.atualizar_telefones(telefones_para_atualizar)

        
        
        ids_telefones_para_deletar = set(mapa_telefones_existentes.keys()) - ids_telefones_recebidos
        
        if ids_telefones_para_deletar:
            FornecedorRepository.deletar_telefones_por_ids(fornecedor, ids_telefones_para_deletar)

        return fornecedor