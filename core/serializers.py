from rest_framework import serializers
from core.models import Fornecedor
import requests
import json


class FornecedorSerializer(serializers.ModelSerializer):
    
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
        
        return Fornecedor.objects.create(**validated_data)

    