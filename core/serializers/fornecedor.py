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
        fields = ['telefone']
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
            validated_data['numero'] = dados_convertidos.get('numero', '')  
            validated_data['complemento'] = dados_convertidos.get('complemento', '')
            validated_data['bairro'] = dados_convertidos.get('bairro', '')
            validated_data['cep'] = dados_convertidos.get('cep', '')
        
        return self.fornecedor_repository.create(**validated_data)
    
    def update(self, instance, validated_data):
        telefones = self.initial_data.get('telefones', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.telefones.all().delete()
        for telefone in telefones:
            instance.telefones.create(telefone=telefone)

        return instance