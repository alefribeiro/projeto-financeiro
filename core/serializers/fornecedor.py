from rest_framework import serializers
from core.models.fornecedor import FornecedorModel, Estado, Cidade
import requests

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['nome', 'uf']


class CidadeSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = Cidade
        fields = ['nome', 'estado']

class FornecedorSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['cidade'] = CidadeSerializer(instance.cidade).data
        return rep
    
    class Meta:
        model = FornecedorModel
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
        
        return FornecedorModel.objects.create(**validated_data)

    